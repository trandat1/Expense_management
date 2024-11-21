from django.contrib import admin
from .models import Profile, History, Expense
# Register your models here.

admin.site.register(Profile)
admin.site.register(History)
admin.site.register(Expense)
