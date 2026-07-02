from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification
from .brevo_utils import send_brevo_email


@receiver(post_save, sender=Notification)
def send_notification_email(sender, instance, created, **kwargs):
    if not created:
        return
    if not instance.user.email:
        return
    send_brevo_email(
        subject=instance.title,
        content=instance.message,
        recipient_list=[instance.user.email],
    )
