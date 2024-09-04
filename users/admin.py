from django.contrib import admin
from django.contrib.auth.models import Group as _DjangoGroup
from users.models import Group, User
from unfold.admin import ModelAdmin

# Register your models here.
# deregister group
admin.site.unregister(_DjangoGroup)
admin.site.register(Group, ModelAdmin)
admin.site.register(User, ModelAdmin)
