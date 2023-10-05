from django.contrib import admin
from django.urls import path

from reviews.admin import CsvImportAdmin
from .models import User


class UserAdmin(admin.ModelAdmin, CsvImportAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'bio',
        'role',
    )

    def get_urls(self):
        urls = super().get_urls()
        urls.insert(-1, path('csv-upload/', self.upload_csv))
        return urls

    def upload_csv(self, request):
        return super().upload_csv(
            request,
            User,
            [
                'id',
                'username',
                'email',
                'role',
                'bio',
                'first_name',
                'last_name',
            ],
        )


admin.site.register(User, UserAdmin)
