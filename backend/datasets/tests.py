from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Dataset


class DatasetApiTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="u1", password="p1")
        self.client = APIClient()

    def _auth(self):
        self.client.force_authenticate(user=self.user)

    def test_auth_required(self):
        res = self.client.get("/api/datasets/")
        self.assertIn(res.status_code, [401, 403])

    def test_upload_and_summary(self):
        self._auth()

        csv = (
            "Equipment Name,Type,Flowrate,Pressure,Temperature\n"
            "Pump A,Pump,10,3,40\n"
            "Reactor 1,Reactor,5,6,120\n"
        ).encode("utf-8")

        file = SimpleUploadedFile("test.csv", csv, content_type="text/csv")
        res = self.client.post("/api/datasets/upload/", data={"file": file}, format="multipart")
        self.assertEqual(res.status_code, 201)
        self.assertIn("dataset", res.data)
        self.assertIn("summary", res.data)

        summary = res.data["summary"]
        self.assertEqual(summary["total_count"], 2)
        self.assertIn("averages", summary)
        self.assertIn("type_distribution", summary)

    def test_list_last_five(self):
        self._auth()

        csv = (
            "Equipment Name,Type,Flowrate,Pressure,Temperature\n"
            "Pump A,Pump,10,3,40\n"
        ).encode("utf-8")

        for i in range(7):
            file = SimpleUploadedFile(f"t{i}.csv", csv, content_type="text/csv")
            res = self.client.post("/api/datasets/upload/", data={"file": file}, format="multipart")
            self.assertEqual(res.status_code, 201)

        qs = Dataset.objects.filter(user=self.user)
        self.assertEqual(qs.count(), 5)

        res = self.client.get("/api/datasets/?limit=5")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data["items"]), 5)

    def test_preview(self):
        self._auth()

        csv = (
            "Equipment Name,Type,Flowrate,Pressure,Temperature\n"
            "Pump A,Pump,10,3,40\n"
            "Pump B,Pump,11,3.2,41\n"
        ).encode("utf-8")

        file = SimpleUploadedFile("test.csv", csv, content_type="text/csv")
        res = self.client.post("/api/datasets/upload/", data={"file": file}, format="multipart")
        dataset_id = res.data["dataset"]["id"]

        res = self.client.get(f"/api/datasets/{dataset_id}/preview/?limit=1")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["preview"]["returned"], 1)

    def test_report_pdf(self):
        self._auth()

        csv = (
            "Equipment Name,Type,Flowrate,Pressure,Temperature\n"
            "Pump A,Pump,10,3,40\n"
        ).encode("utf-8")

        file = SimpleUploadedFile("test.csv", csv, content_type="text/csv")
        res = self.client.post("/api/datasets/upload/", data={"file": file}, format="multipart")
        dataset_id = res.data["dataset"]["id"]

        res = self.client.get(f"/api/datasets/{dataset_id}/report.pdf")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res["Content-Type"], "application/pdf")
