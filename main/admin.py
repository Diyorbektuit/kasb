from django.contrib import admin
from django.contrib.auth.models import Group, User
from main import models

# Register your models here.
admin.site.unregister(Group)
admin.site.unregister(User)

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_uz', 'name_eng', 'name_ru', 'order')


@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_uz', 'name_eng', 'name_ru')


@admin.register(models.Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_uz', 'name_eng', 'name_ru')


@admin.register(models.Vacancy)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title_eng', 'company', 'category', 'country')
    list_filter = ('job_schedule', 'work_location')


@admin.register(models.Application)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'fullname', 'phone_number', 'email', 'country', 'vacancy')
    list_filter = ('country', 'vacancy')


@admin.register(models.Post)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title_eng', 'poster', 'slug')
    readonly_fields = ('slug', )


@admin.register(models.Form)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'fullname', 'phone_number', 'description')
    search_fields = ('fullname', 'phone_number')