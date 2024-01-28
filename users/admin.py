from django.contrib import admin

# from django.contrib.admin import ModelAdmin
from django import forms
from django.db import models
from unfold.admin import ModelAdmin
from django.contrib.auth.models import Group as _Group
from users.models import Group, User

# Register your models here.
admin.site.unregister(_Group)


@admin.register(Group)
class GroupAdmin(ModelAdmin):
    formfield_overrides = {
        models.ManyToManyField: {"widget": forms.CheckboxSelectMultiple},
    }
    pass


@admin.register(User)
class UserAdmin(ModelAdmin):
    class GroupInline(admin.TabularInline):
        model = Group

    list_display = ["username", "display_groups", "last_login", "is_staff"]

    formfield_overrides = {
        models.ManyToManyField: {"widget": forms.CheckboxSelectMultiple},
    }

    @admin.display(description="Groups")
    def display_groups(self, obj):
        return ", ".join([g.name for g in obj.groups.all()])

    pass
