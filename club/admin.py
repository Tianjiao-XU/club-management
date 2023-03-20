from django.contrib import admin
from club.models import Club, User, Approval

# Register your models here.

admin.site.register(User)
admin.site.register(Club)
admin.site.register(Approval)


