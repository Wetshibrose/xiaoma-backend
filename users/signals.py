from django.db.models.signals import post_delete, post_save, pre_delete
from django.dispatch import receiver

from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from .models import CustomUser


@receiver(signal=post_save, sender=CustomUser)
def log_user_creation(sender, instance: CustomUser, created: bool, **kwargs):
    if created:
        contenttype = ContentType.objects.get_for_model(instance)
        try:
            LogEntry.objects.create(
                user=instance,
                content_type=contenttype,
                object_id=instance.id,
                object_repr=str(instance),
                action_flag=ADDITION,
                change_message="New user created",
            )
        except Exception as error:
            print(error)
        
