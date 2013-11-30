from django.contrib import admin
from models import AdditionalUserInfo, Report

class UserAdmin(admin.ModelAdmin):
    list_display = ('user', 'spamCount')

admin.site.register(AdditionalUserInfo, UserAdmin)
admin.site.register(Report)
