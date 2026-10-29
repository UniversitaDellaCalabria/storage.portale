from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from laboratories.models import LaboratorioDatiBase


@receiver(post_delete, sender=LaboratorioDatiBase)
def delete_logo_on_laboratory_delete(sender, instance, **kwargs):
    """Rimuove il file del logo quando il laboratorio viene eliminato."""
    if instance.nome_file_logo:
        instance.nome_file_logo.delete(save=False)


@receiver(pre_save, sender=LaboratorioDatiBase)
def delete_old_logo_on_change(sender, instance, **kwargs):
    """Rimuove il vecchio logo quando viene sostituito o cancellato."""
    if not instance.pk:
        return

    old_name = (
        sender.objects.filter(pk=instance.pk)
        .values_list("nome_file_logo", flat=True)
        .first()
    )
    if old_name and old_name != instance.nome_file_logo.name:
        instance.nome_file_logo.storage.delete(old_name)
