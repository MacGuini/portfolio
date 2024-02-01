from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Comment
from . import mail_control

@receiver(post_save, sender=Comment)
def repliedComment(sender, instance, created, **kwargs):
    print("\n\n\nSignal triggered\n\n\n")
    comment = instance 

    mail_control.commentReplied(comment)

