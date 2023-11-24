from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from .models import Profile
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.http.response import HttpResponseForbidden


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.get_or_create(user=instance)  # sử dụng key được sinh ra


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


# @receiver(pre_save, sender=User)
# def check_unique_email(sender, instance, **kwargs):
#     if User.objects.filter(email=instance.email).exclude(pk=instance.pk).exists():
#         raise ValidationError("A user with that email already exists.")


# @receiver(pre_save, sender=User)
# def check_token_before_update(sender, instance, **kwargs):
#     token = Token.objects.filter(user=instance)
#     if token[0].user_id != instance.id:
#         raise HttpResponseForbidden("bạn không có quyền cập nhật.")
