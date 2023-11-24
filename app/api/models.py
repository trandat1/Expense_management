from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class Profile(models.Model):
    GENDER_CHOICES = (
        ("M", "Male"),
        ("F", "Female"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to="frontend/static/images/uploads",
        default="static/images/uploads/account-icon-user-icon-vector-graphics_292645-552.avif",
        max_length=255,
    )
    sex = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)
    birth = models.DateField(null=True)


# @receiver(post_save, sender=User)
# def create_user_token(sender, instance, created, **kwargs):
#     if created:
#         Token.objects.get_or_create(user=instance)


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    rent = models.FloatField()
    food = models.FloatField()
    saving = models.FloatField()
    other = models.FloatField()
    date = models.DateField()


class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.FloatField()
    description = models.TextField()
    field = models.CharField(max_length=50)
