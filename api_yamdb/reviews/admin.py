import csv
from django.db.models.fields.related import ForeignKey
from django.contrib import admin
from django.urls import path
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from .forms import CsvImportForm
from .models import (
    Title,
    Category,
    Genre,
    Review,
    Comments,
    GengeTitle,
)


class CsvImportAdmin:
    """Скрипт для импорта файлов csv формата через админ панель."""

    def upload_csv(self, request, model, fields):
        if request.method == 'POST':
            form = CsvImportForm(request.POST, request.FILES)
            if form.is_valid():
                # валидация формы
                form_object = form.save()
                form_object.save()
                with form_object.csv_file.open('r') as csv_file:
                    rows = csv.reader(csv_file, delimiter=',')
                    if next(rows) != fields:
                        messages.warning(request, 'Неверные заголовки у файла')
                        return HttpResponseRedirect(request.path_info)

                    for row in list(rows):
                        model_atribute = {}
                        # Отлавливаем имена полей с FK, что бы адаптировать
                        # для полей в базе
                        fields_fk = [
                            f.name
                            for f in model._meta.get_fields()
                            if isinstance(f, ForeignKey)
                        ]
                        for indx in range(len(fields)):
                            if fields[indx] in fields_fk:
                                model_atribute[
                                    f'{fields[indx] + "_id"}'
                                ] = row[indx]
                            else:
                                model_atribute[fields[indx]] = row[indx]

                        if issubclass(Comments, model):
                            # Для модели Сomment подтягиваем pk title
                            review_obj = Review.objects.get(
                                id=model_atribute.get('review_id')
                            )
                            model_atribute['title_id'] = review_obj.title_id

                        model.objects.update_or_create(**model_atribute)
                url = reverse('admin:index')
                messages.success(request, 'Файл успешно импортирован')
                return HttpResponseRedirect(url)
        form = CsvImportForm()
        return render(request, 'admin/csv_import_page.html', {'form': form})


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin, CsvImportAdmin):
    def get_urls(self):
        urls = super().get_urls()
        urls.insert(-1, path('csv-upload/', self.upload_csv))
        return urls

    def upload_csv(self, request):
        return super().upload_csv(
            request,
            Genre,
            ['id', 'name', 'slug'],
        )


@admin.register(GengeTitle)
class GengeTitleAdmin(admin.ModelAdmin, CsvImportAdmin):
    def get_urls(self):
        urls = super().get_urls()
        urls.insert(-1, path('csv-upload/', self.upload_csv))
        return urls

    def upload_csv(self, request):
        return super().upload_csv(
            request,
            GengeTitle,
            ['id', 'title_id', 'genre_id'],
        )


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin, CsvImportAdmin):
    def get_urls(self):
        urls = super().get_urls()
        urls.insert(-1, path('csv-upload/', self.upload_csv))
        return urls

    def upload_csv(self, request):
        return super().upload_csv(
            request,
            Title,
            ['id', 'name', 'year', 'category'],
        )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin, CsvImportAdmin):
    def get_urls(self):
        urls = super().get_urls()
        urls.insert(-1, path('csv-upload/', self.upload_csv))
        return urls

    def upload_csv(self, request):
        return super().upload_csv(
            request,
            Category,
            ['id', 'name', 'slug'],
        )


@admin.register(Review)
class ReviewsAdmin(admin.ModelAdmin, CsvImportAdmin):
    def get_urls(self):
        urls = super().get_urls()
        urls.insert(-1, path('csv-upload/', self.upload_csv))
        return urls

    def upload_csv(self, request):
        return super().upload_csv(
            request,
            Review,
            ['id', 'title_id', 'text', 'author', 'score', 'pub_date'],
        )


@admin.register(Comments)
class CommentAdmin(admin.ModelAdmin, CsvImportAdmin):
    def get_urls(self):
        urls = super().get_urls()
        urls.insert(-1, path('csv-upload/', self.upload_csv))
        return urls

    def upload_csv(self, request):
        return super().upload_csv(
            request,
            Comments,
            ['id', 'review_id', 'text', 'author', 'pub_date'],
        )
