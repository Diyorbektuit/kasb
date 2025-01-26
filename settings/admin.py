from django.contrib import admin

from main.admin import MultiLanguageAdmin
from settings import models
# Register your models here.

@admin.register(models.Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code')

# Category Admin
class CategoryLanguageInline(admin.TabularInline):
    model = models.CategoryLanguage
    extra = 0
    can_delete = False
    fields = ('language', 'name',)
    readonly_fields = ('language',)

@admin.register(models.Category)
class CategoryAdmin(MultiLanguageAdmin):
    list_display = ('id', 'order')
    translation_model = models.CategoryLanguage
    translation_fk_field = 'category'
    inlines = (CategoryLanguageInline, )


# Company Admin
class CompanyLanguageInline(admin.TabularInline):
    model = models.CompanyLanguage
    extra = 1  # Bo'sh joylar yaratish
    fields = ['language', 'name']
    readonly_fields = ['language']  # Tillarni faqat o‘qish uchun qoldiramiz

@admin.register(models.Company)
class CompanyAdmin(MultiLanguageAdmin):
    list_display = ('id', 'image')
    translation_model = models.CompanyLanguage
    translation_fk_field = 'company'
    inlines = (CompanyLanguageInline, )


# Country Admin
class CountryLanguageInline(admin.TabularInline):
    model = models.CountryLanguage
    extra = 0
    can_delete = False
    fields = ['language', 'name']
    readonly_fields = ['language']

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(models.Country)
class CountryAdmin(MultiLanguageAdmin):
    list_display = ('id', 'icon')
    translation_model = models.CountryLanguage
    translation_fk_field = 'country'
    inlines = (CountryLanguageInline, )


# General Information
class GeneralInformationLanguageInline(admin.StackedInline):
    model = models.GeneralInformationLanguage
    extra = 0
    can_delete = False
    fields = ['language', 'headline', 'description', 'address', 'opening_hours']
    readonly_fields = ['language']

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(models.GeneralInformation)
class GeneralInformationAdmin(MultiLanguageAdmin):
    list_display = ('email', 'phone', 'telegram', 'instagram', 'facebook', 'youtube')
    translation_model = models.GeneralInformationLanguage
    translation_fk_field = 'general_information'
    inlines = (GeneralInformationLanguageInline, )

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
