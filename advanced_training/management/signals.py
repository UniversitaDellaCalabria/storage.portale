from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from advanced_training.models import AltaFormazioneDatiBase
import os

@receiver(post_delete, sender=AltaFormazioneDatiBase)
def delete_master_files(sender, instance, **kwargs):
    """Elimina i file fisici quando viene eliminato un master"""
    if instance.path_piano_finanziario:
        if os.path.isfile(instance.path_piano_finanziario.path):
            os.remove(instance.path_piano_finanziario.path)
    
    if instance.path_doc_delibera:
        if os.path.isfile(instance.path_doc_delibera.path):
            os.remove(instance.path_doc_delibera.path)