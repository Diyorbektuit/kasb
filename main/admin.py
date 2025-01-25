from django.contrib import admin
from django.contrib.auth.models import Group, User
from main import models

# Register your models here.
admin.site.unregister(Group)
admin.site.unregister(User)

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_uz', 'name_eng', 'name_ru', 'order')
    search_fields = ('name_uz', 'name_eng', 'name_ru')


@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_uz', 'name_eng', 'name_ru')
    search_fields = ('name_uz', 'name_eng', 'name_ru')


@admin.register(models.Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_uz', 'name_eng', 'name_ru')
    search_fields = ('name_uz', 'name_eng', 'name_ru')


class ApplicationInline(admin.TabularInline):
    model = models.Application
    extra = 0
    can_delete = False
    fields = ('id', 'fullname', 'phone_number', 'email', 'extra_description')
    readonly_fields = ('fullname', 'phone_number', 'email', 'extra_description')

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(models.Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('id', 'title_eng', 'company', 'category', 'country')
    list_filter = ('job_schedule', 'work_location', 'category', 'country', 'company')
    search_fields = ('title_uz', 'title_eng', 'title_ru')
    inlines = (ApplicationInline, )


@admin.register(models.Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'fullname', 'phone_number', 'email', 'country', 'vacancy')
    list_filter = ('country', 'vacancy')
    search_fields = ('fullname', 'phone_number', 'email')


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title_eng', 'poster', 'slug')
    readonly_fields = ('slug', )
    search_fields = ('title_uz', 'title_eng', 'title_ru')


@admin.register(models.Form)
class FormAdmin(admin.ModelAdmin):
    list_display = ('id', 'fullname', 'phone_number', 'description')
    search_fields = ('fullname', 'phone_number')