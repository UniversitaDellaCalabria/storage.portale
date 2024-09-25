from companies.models import SpinoffStartupDatiBase
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver


@receiver(post_delete, sender=SpinoffStartupDatiBase)
def post_save_image(sender, instance, *args, **kwargs):
    """Clean Old Image file"""
    try:
        instance.nome_file_logo.delete(save=False)
    except Exception:
        pass


@receiver(pre_save, sender=SpinoffStartupDatiBase)
def pre_save_image(sender, instance, *args, **kwargs):
    """instance old image file will delete from os"""
    try:
        old = instance.__class__.objects.get(id=instance.id).nome_file_logo.path
        try:
            new = instance.nome_file_logo.path
        except Exception:
            new = None
        if new != old:
            import os

            if os.path.exists(old):
                os.remove(old)
    except Exception:
        pass
