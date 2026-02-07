from django.urls import path

from .views import (
    DatasetListView,
    DatasetPreviewView,
    DatasetReportPdfView,
    DatasetSummaryView,
    DatasetUploadView,
    MeView,
)

urlpatterns = [
    path("me/", MeView.as_view(), name="me"),
    path("datasets/", DatasetListView.as_view(), name="datasets-list"),
    path("datasets/upload/", DatasetUploadView.as_view(), name="datasets-upload"),
    path("datasets/<uuid:dataset_id>/summary/", DatasetSummaryView.as_view(), name="datasets-summary"),
    path("datasets/<uuid:dataset_id>/preview/", DatasetPreviewView.as_view(), name="datasets-preview"),
    path("datasets/<uuid:dataset_id>/report.pdf", DatasetReportPdfView.as_view(), name="datasets-report"),
]
