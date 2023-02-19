from django.contrib import admin

from .models import User


class UserAdminFilter(admin.ModelAdmin):
    list_filter = ["email", "username", ]


admin.site.register(User, UserAdminFilter)
