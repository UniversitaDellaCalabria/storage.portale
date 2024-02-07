from django.db.models.signals import *
from django.dispatch import receiver

from ricerca_app.models import SitoWebCdsExStudenti


@receiver(post_delete, sender=SitoWebCdsExStudenti)
def post_save_image(sender, instance, *args, **kwargs):
    """ Clean Old Image file """
    try:
        instance.foto.delete(save=False)
    except:
        pass


@receiver(pre_save, sender=SitoWebCdsExStudenti)
def pre_save_image(sender, instance, *args, **kwargs):
    """ instance old image file will delete from os """
    try:
        old = instance.__class__.objects.get(id=instance.id).foto.path
        try:
            new = instance.foto.path
        except:
            new = None
        if new != old:
            import os
            if os.path.exists(old):
                os.remove(old)
    except:
        pass
