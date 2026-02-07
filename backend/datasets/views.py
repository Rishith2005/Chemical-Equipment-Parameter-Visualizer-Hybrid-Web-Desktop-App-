from __future__ import annotations

from io import BytesIO

import pandas as pd
from django.http import FileResponse, Http404
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Dataset, DatasetSummary
from .serializers import DatasetSerializer
from .services import compute_summary_analytics, preview_rows


class MeView(APIView):
    def get(self, request):
        user = request.user
        return Response({"id": user.id, "username": user.username})


class DatasetUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        upload = request.data.get("file")
        if upload is None:
            return Response({"detail": "Missing file"}, status=400)

        dataset = Dataset.objects.create(
            user=request.user,
            filename=getattr(upload, "name", "dataset.csv"),
            status=Dataset.Status.PROCESSING,
            csv_file=upload,
        )

        try:
            df = pd.read_csv(dataset.csv_file.path)
            analytics = compute_summary_analytics(df)
            dataset.row_count = int(len(df))
            dataset.column_count = int(len(df.columns))
            dataset.status = Dataset.Status.READY
            dataset.last_error = ""
            dataset.save(update_fields=[
                "row_count",
                "column_count",
                "status",
                "last_error",
            ])

            summary = DatasetSummary.objects.create(
                dataset=dataset,
                user=request.user,
                summary_json=analytics.to_json(),
            )
        except Exception as e:
            dataset.status = Dataset.Status.ERROR
            dataset.last_error = str(e)
            dataset.save(update_fields=["status", "last_error"])
            return Response({"detail": "CSV processing failed", "error": str(e)}, status=400)

        self._enforce_last_five(request.user)

        return Response(
            {
                "dataset": DatasetSerializer(dataset).data,
                "summary": summary.summary_json,
            },
            status=201,
        )

    def _enforce_last_five(self, user) -> None:
        keep = list(Dataset.objects.filter(user=user).order_by("-uploaded_at")[:5])
        keep_ids = [d.id for d in keep]
        Dataset.objects.filter(user=user).exclude(id__in=keep_ids).delete()


class DatasetListView(APIView):
    def get(self, request):
        try:
            limit = int(request.query_params.get("limit", "5"))
        except ValueError:
            limit = 5
        limit = max(1, min(limit, 5))

        items = Dataset.objects.filter(user=request.user).order_by("-uploaded_at")[:limit]
        return Response({"items": DatasetSerializer(items, many=True).data})


class DatasetSummaryView(APIView):
    def get(self, request, dataset_id: str):
        try:
            dataset = Dataset.objects.get(id=dataset_id, user=request.user)
        except Dataset.DoesNotExist:
            raise Http404

        summary = dataset.summaries.first()
        if summary is None:
            return Response({"detail": "Summary not found"}, status=404)

        return Response({"dataset": DatasetSerializer(dataset).data, "summary": summary.summary_json})


class DatasetPreviewView(APIView):
    def get(self, request, dataset_id: str):
        try:
            dataset = Dataset.objects.get(id=dataset_id, user=request.user)
        except Dataset.DoesNotExist:
            raise Http404

        try:
            limit = int(request.query_params.get("limit", "50"))
        except ValueError:
            limit = 50

        df = pd.read_csv(dataset.csv_file.path)
        return Response({"dataset": DatasetSerializer(dataset).data, "preview": preview_rows(df, limit)})


class DatasetReportPdfView(APIView):
    def get(self, request, dataset_id: str):
        try:
            dataset = Dataset.objects.get(id=dataset_id, user=request.user)
        except Dataset.DoesNotExist:
            raise Http404

        summary = dataset.summaries.first()
        summary_json = summary.summary_json if summary else {}

        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        y = height - 0.75 * inch
        c.setFont("Helvetica-Bold", 16)
        c.drawString(0.75 * inch, y, "Chemical Equipment Dataset Report")

        y -= 0.5 * inch
        c.setFont("Helvetica", 11)
        c.drawString(0.75 * inch, y, f"Filename: {dataset.filename}")
        y -= 0.25 * inch
        c.drawString(0.75 * inch, y, f"Uploaded: {dataset.uploaded_at.isoformat()}")
        y -= 0.25 * inch
        c.drawString(0.75 * inch, y, f"Rows: {dataset.row_count or '-'}  Columns: {dataset.column_count or '-'}")

        y -= 0.5 * inch
        c.setFont("Helvetica-Bold", 12)
        c.drawString(0.75 * inch, y, "Summary")
        y -= 0.3 * inch
        c.setFont("Helvetica", 11)

        total = summary_json.get("total_count")
        c.drawString(0.75 * inch, y, f"Total equipment count: {total if total is not None else '-'}")
        y -= 0.25 * inch

        averages = summary_json.get("averages") or {}
        for key in ["Flowrate", "Pressure", "Temperature"]:
            val = averages.get(key)
            c.drawString(0.75 * inch, y, f"Average {key}: {val if val is not None else '-'}")
            y -= 0.25 * inch

        y -= 0.25 * inch
        c.setFont("Helvetica-Bold", 12)
        c.drawString(0.75 * inch, y, "Equipment Type Distribution")
        y -= 0.3 * inch
        c.setFont("Helvetica", 11)

        distribution = summary_json.get("type_distribution") or {}
        for t, count in sorted(distribution.items(), key=lambda x: (-x[1], x[0])):
            c.drawString(0.75 * inch, y, f"{t}: {count}")
            y -= 0.22 * inch
            if y < 0.75 * inch:
                c.showPage()
                y = height - 0.75 * inch
                c.setFont("Helvetica", 11)

        c.showPage()
        c.save()

        buffer.seek(0)
        filename = f"dataset_{dataset.id}.pdf"
        return FileResponse(buffer, as_attachment=True, filename=filename, content_type="application/pdf")
