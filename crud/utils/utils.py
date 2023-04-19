from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType


def log_action(user, obj, flag, msg):
    LogEntry.objects.log_action(user_id=user.pk,
                                content_type_id=ContentType.objects.get_for_model(
                                    obj).pk,
                                object_id=obj.pk,
                                object_repr=obj.__str__(),
                                action_flag=flag,
                                change_message=msg)


def _clean_teacher_dates(obj, cleaned_data):
    dt_inizio = cleaned_data.get('dt_inizio')
    dt_fine = cleaned_data.get('dt_fine')

    if dt_inizio and dt_fine and dt_inizio > dt_fine:
        obj.add_error('dt_inizio',
                      _("Start date is greater than end date"))
        obj.add_error('dt_fine',
                      _("Start date is greater than end date"))
