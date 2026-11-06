from django.db import transaction
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from laboratories_new.models import LaboratorioDatiBase


def _delete_file_on_commit(storage, name):
    """Cancella il file solo se la transazione corrente va a buon fine."""
    if not name:
        return
    transaction.on_commit(lambda: storage.delete(name))


@receiver(post_delete, sender=LaboratorioDatiBase)
def delete_logo_on_laboratory_delete(sender, instance, **kwargs):
    """Rimuove il file del logo quando il laboratorio viene eliminato."""
    if instance.nome_file_logo:
        _delete_file_on_commit(
            instance.nome_file_logo.storage, instance.nome_file_logo.name
        )


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
        _delete_file_on_commit(instance.nome_file_logo.storage, old_name)
