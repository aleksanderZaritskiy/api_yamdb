from django.contrib import admin
from django.urls import path
from django.contrib.auth.admin import UserAdmin

from reviews.admin import CsvImportAdmin
from .models import MyUser


class MyUserAdmin(UserAdmin):
    def get_urls(self):
        urls = super().get_urls()
        urls.insert(-1, path('csv-upload/', self.upload_csv))
        return urls

    def upload_csv(self, request):
        return CsvImportAdmin.import_csv_file(
            self,
            request,
            MyUser,
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


UserAdmin.fieldsets += (('Extra Fields', {'fields': ('bio', 'role')}),)

admin.site.register(MyUser, MyUserAdmin)
