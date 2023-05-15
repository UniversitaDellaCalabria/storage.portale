from django.db.models.signals import *
from django.dispatch import receiver

from ricerca_app.models import BrevettoDatiBase


@receiver(post_delete, sender=BrevettoDatiBase)
def post_save_image(sender, instance, *args, **kwargs):
    """ Clean Old Image file """
    try:
        instance.nome_file_logo.delete(save=False)
    except:
        pass


@receiver(pre_save, sender=BrevettoDatiBase)
def pre_save_image(sender, instance, *args, **kwargs):
    """ instance old image file will delete from os """
    try:
        old = instance.__class__.objects.get(id=instance.id).nome_file_logo.path
        try:
            new = instance.nome_file_logo.path
        except:
            new = None
        if new != old:
            import os
            if os.path.exists(old):
                os.remove(old)
    except:
        pass
