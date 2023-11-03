from django.db import models
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token

# Create your models here.


class Customers(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    image = models.ImageField(
        upload_to="images/upload",
        default="account-icon-user-icon-vector-graphics_292645-552.avif",
        max_length=255,
    )

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super(Customers, self).save(*args, **kwargs)
        if self.user.is_superuser:
            # Tạo token cho superuser
            Token.objects.get_or_create(user=self.user)


class Expense(models.Model):
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    amount = models.FloatField()
    rent = models.FloatField()
    food = models.FloatField()
    saving = models.FloatField()
    other = models.FloatField()
    date = models.DateField()


class History(models.Model):
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.FloatField()
    description = models.TextField()
    field = models.CharField(max_length=50)
