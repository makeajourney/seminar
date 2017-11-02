from django.contrib import admin

from .models import EmailToken, EmailUser, Profile


class EmailTokenAdmin(admin.ModelAdmin):
    list_display = ('email', 'token', 'created_at')
    search_fields = ('email',)


admin.site.register(EmailToken, EmailTokenAdmin)
admin.site.register(EmailUser)
admin.site.register(Profile)
