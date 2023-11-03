from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        if instance.is_superuser:
            Token.objects.create(user=instance, key="superuser_key")
        else:
            Token.objects.create(user=instance)  # sử dụng key được sinh ra