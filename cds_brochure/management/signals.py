from cds_brochure.models import CdsBrochureExStudenti
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver


@receiver(post_delete, sender=CdsBrochureExStudenti)
def post_save_image(sender, instance, *args, **kwargs):
    """Clean Old Image file"""
    try:
        instance.foto.delete(save=False)
    except Exception:
        pass


@receiver(pre_save, sender=CdsBrochureExStudenti)
def pre_save_image(sender, instance, *args, **kwargs):
    """instance old image file will delete from os"""
    try:
        old = instance.__class__.objects.get(id=instance.id).foto.path
        try:
            new = instance.foto.path
        except Exception:
            new = None
        if new != old:
            import os

            if os.path.exists(old):
                os.remove(old)
    except Exception:
        pass
