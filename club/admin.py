from django.contrib import admin
from django.contrib.auth.models import User

from club.models import UserProfile,Club


# Register your models here.

admin.site.register(UserProfile)
# admin.site.register(User)
admin.site.register(Club)


