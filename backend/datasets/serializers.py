from rest_framework import serializers

from .models import Dataset, DatasetSummary


class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = [
            "id",
            "filename",
            "status",
            "row_count",
            "column_count",
            "uploaded_at",
        ]


class DatasetSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = DatasetSummary
        fields = [
            "id",
            "dataset",
            "summary_json",
            "generated_at",
        ]
