import os

from django.db.models.signals import *
from django.dispatch import receiver

from ricerca_app.models import DidatticaCdsAltriDati


@receiver(pre_save, sender=DidatticaCdsAltriDati)
def pre_save_manifesto_studi(sender, instance, *args, **kwargs):
    """ instance old image file will delete from os """
    try:
        old = instance.__class__.objects.get(id=instance.id).manifesto_studi.path
        try:
            new = instance.manifesto_studi.path
        except:
            new = None
        if new != old:
            if os.path.exists(old):
                os.remove(old)
    except:
        pass

@receiver(pre_save, sender=DidatticaCdsAltriDati)
def pre_save_regolamento_didattico(sender, instance, *args, **kwargs):
    """ instance old image file will delete from os """
    try:
        old = instance.__class__.objects.get(id=instance.id).regolamento_didattico.path
        try:
            new = instance.regolamento_didattico.path
        except:
            new = None
        if new != old:
            if os.path.exists(old):
                os.remove(old)
    except:
        pass

@receiver(pre_save, sender=DidatticaCdsAltriDati)
def pre_save_ordinamento_didattico(sender, instance, *args, **kwargs):
    """ instance old image file will delete from os """
    try:
        old = instance.__class__.objects.get(id=instance.id).ordinamento_didattico.path
        try:
            new = instance.ordinamento_didattico.path
        except:
            new = None
        if new != old:
            if os.path.exists(old):
                os.remove(old)
    except:
        pass
