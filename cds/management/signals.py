import os

from cds.models import DidatticaCdsAltriDati
from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(pre_save, sender=DidatticaCdsAltriDati)
def pre_save_manifesto_studi(sender, instance, *args, **kwargs):
    """instance old image file will delete from os"""
    try:
        old = instance.__class__.objects.get(pk=instance.pk).manifesto_studi.path
        try:
            new = instance.manifesto_studi.path
        except Exception:
            new = None
        if new != old:
            if os.path.exists(old):
                os.remove(old)
    except Exception:
        pass


@receiver(pre_save, sender=DidatticaCdsAltriDati)
def pre_save_regolamento_didattico(sender, instance, *args, **kwargs):
    """instance old image file will delete from os"""
    try:
        old = instance.__class__.objects.get(pk=instance.pk).regolamento_didattico.path
        try:
            new = instance.regolamento_didattico.path
        except Exception:
            new = None
        if new != old:
            if os.path.exists(old):
                os.remove(old)
    except Exception:
        pass


@receiver(pre_save, sender=DidatticaCdsAltriDati)
def pre_save_ordinamento_didattico(sender, instance, *args, **kwargs):
    """instance old image file will delete from os"""
    try:
        old = instance.__class__.objects.get(pk=instance.pk).ordinamento_didattico.path
        try:
            new = instance.ordinamento_didattico.path
        except Exception:
            new = None
        if new != old:
            if os.path.exists(old):
                os.remove(old)
    except Exception:
        pass
