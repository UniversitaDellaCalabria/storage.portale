import os

from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from teachers.models import DocentePtaAltriDati


@receiver(post_delete, sender=DocentePtaAltriDati)
def post_save_image(sender, instance, *args, **kwargs):
    """Clean Old Image file"""
    try:
        instance.path_foto.delete(save=False)
    except Exception:
        pass


@receiver(post_delete, sender=DocentePtaAltriDati)
def post_save_cvita(sender, instance, *args, **kwargs):
    """Clean Old Image file"""
    try:
        instance.path_cv_ita.delete(save=False)
    except Exception:
        pass


@receiver(post_delete, sender=DocentePtaAltriDati)
def post_save_cven(sender, instance, *args, **kwargs):
    """Clean Old Image file"""
    try:
        instance.path_cv_en.delete(save=False)
    except Exception:
        pass


@receiver(pre_save, sender=DocentePtaAltriDati)
def pre_save_image(sender, instance, *args, **kwargs):
    """instance old image file will delete from os"""
    try:
        old = instance.__class__.objects.get(id=instance.id).path_foto.path
        try:
            new = instance.path_foto.path
        except Exception:
            new = None
        if new != old:
            if os.path.exists(old):
                os.remove(old)
    except Exception:
        pass


@receiver(pre_save, sender=DocentePtaAltriDati)
def pre_save_cvita(sender, instance, *args, **kwargs):
    """instance old image file will delete from os"""
    try:
        old = instance.__class__.objects.get(id=instance.id).path_cv_ita.path
        try:
            new = instance.path_cv_ita.path
        except Exception:
            new = None
        if new != old:
            if os.path.exists(old):
                os.remove(old)
    except Exception:
        pass


@receiver(pre_save, sender=DocentePtaAltriDati)
def pre_save_cven(sender, instance, *args, **kwargs):
    """instance old image file will delete from os"""
    try:
        old = instance.__class__.objects.get(id=instance.id).path_cv_en.path
        try:
            new = instance.path_cv_en.path
        except Exception:
            new = None
        if new != old:
            if os.path.exists(old):
                os.remove(old)
    except Exception:
        pass
