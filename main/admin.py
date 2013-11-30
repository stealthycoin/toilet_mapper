from django.contrib import admin
from models import AdditionalUserInfo

class UserAdmin(admin.ModelAdmin):
    list_display = ('user', 'spamCount')

admin.site.register(AdditionalUserInfo, UserAdmin)
