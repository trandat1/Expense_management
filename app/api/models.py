from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date

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
    # @staticmethod
    def __str__(self):
        return self.user.username

# @receiver(post_save, sender=User)
# def create_user_token(sender, instance, created, **kwargs):
#     if created:
#         Token.objects.get_or_create(user=instance)


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    rent = models.FloatField(null=True)
    food = models.FloatField(null=True)
    saving = models.FloatField(null=True, blank=True)  # Cho phép lưu giá trị null nếu không có giá trị
    other = models.FloatField(null=True)
    date = models.DateField(null=True)

    def save(self, *args, **kwargs):
        # Tính toán giá trị saving nếu chưa có giá trị
        if self.saving is None:  # Chỉ tính toán nếu saving chưa có giá trị
            self.saving = self.amount - (self.rent or 0) - (self.food or 0) - (self.other or 0) 
        super().save(*args, **kwargs)  # Lưu đối tượng sau khi tính toán

    def __str__(self):
        return self.user.username

class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    FIELD_CHOICES = (
        ("R", "Rent"),
        ("F", "Food"),
        ("S", "Saving"),
        ("O", "Other"),
    )
    date = models.DateField(default=date.today())
    amount = models.FloatField()
    description = models.TextField(null=True)
    field = models.CharField(max_length=1, choices=FIELD_CHOICES, null=True)
    balance = models.FloatField(editable=False, null = True)
    # @staticmethod
    def __str__(self):
        return f"{self.user.username} ({self.date})"