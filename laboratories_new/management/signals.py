from django.db import transaction
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from laboratories_new.models import LaboratorioDatiBase
from laboratories_new.snapshot_service import published_logo_names


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
    if not old_name or old_name == instance.nome_file_logo.name:
        return

    # Lo snapshot NON viene rigenerato con la modifica, ma solo all'approvazione:
    # se il vecchio logo e' quello della versione pubblicata, l'API lo usa
    # ancora e va tenuto (lo cancella refresh_snapshot quando viene sostituito).
    # Altrimenti era solo un logo intermedio non approvato e si puo' cancellare.
    if old_name in published_logo_names(instance.pk):
        return
    _delete_file_on_commit(instance.nome_file_logo.storage, old_name)
