from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import Dataset


@receiver(post_delete, sender=Dataset)
def delete_dataset_files(sender, instance: Dataset, **kwargs):
    if instance.csv_file:
        instance.csv_file.delete(save=False)
    if instance.pdf_report:
        instance.pdf_report.delete(save=False)
