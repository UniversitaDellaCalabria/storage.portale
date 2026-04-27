from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from advanced_training.models import AltaFormazioneDatiBase, AltaFormazioneIncaricoDidattico
import os


@receiver(pre_save, sender=AltaFormazioneDatiBase)
def delete_old_master_files_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return False

    # Lista dei campi file da monitorare
    file_fields = ['path_piano_finanziario', 'path_doc_delibera']

    for field_name in file_fields:
        old_file = getattr(old_instance, field_name)
        new_file = getattr(instance, field_name)

        # Se il file è cambiato (o rimosso), eliminiamo il vecchio dal disco
        if old_file and old_file != new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)

            
@receiver(post_delete, sender=AltaFormazioneDatiBase)
def delete_master_files(sender, instance, **kwargs):
    """Elimina i file fisici quando viene eliminato un master"""
    if instance.path_piano_finanziario:
        if os.path.isfile(instance.path_piano_finanziario.path):
            os.remove(instance.path_piano_finanziario.path)
    
    if instance.path_doc_delibera:
        if os.path.isfile(instance.path_doc_delibera.path):
            os.remove(instance.path_doc_delibera.path)



@receiver(pre_save, sender=AltaFormazioneIncaricoDidattico)
def delete_old_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        # Recuperiamo l'oggetto "vecchio" dal database
        old_file = sender.objects.get(pk=instance.pk).path_cv
    except sender.DoesNotExist:
        return False

    # Confrontiamo il nuovo file con quello vecchio
    new_file = instance.path_cv
    if not old_file == new_file:
        if old_file and os.path.isfile(old_file.path):
            os.remove(old_file.path)

            
@receiver(post_delete, sender=AltaFormazioneIncaricoDidattico)
def delete_cv(sender, instance, **kwargs):
    """Elimina i file fisici quando viene eliminato un master"""
    if instance.path_cv:
        if os.path.isfile(instance.path_cv.path):
            os.remove(instance.path_cv.path)
