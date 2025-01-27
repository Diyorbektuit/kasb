from django.contrib import admin

from main.admin import MultiLanguageAdmin
from settings import models
from settings.models import Language


# Register your models here.
class DynamicGeneralInformationLanguageInline(admin.StackedInline):
    model = models.GeneralInformationLanguage
    extra = 0
    can_delete = False
    fields = ['language', 'headline', 'description', 'opening_hours', 'address']
    readonly_fields = ['language']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if hasattr(self, "language_code"):
            queryset = queryset.filter(language__code=self.language_code)
        return queryset

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


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

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(models.Category)
class CategoryAdmin(MultiLanguageAdmin):
    list_display = ('id', 'order')
    translation_model = models.CategoryLanguage
    translation_fk_field = 'category'
    inlines = (CategoryLanguageInline, )


# Company Admin
class CompanyLanguageInline(admin.TabularInline):
    model = models.CompanyLanguage
    extra = 0
    fields = ['language', 'name']
    readonly_fields = ['language']

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


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

    def get_inlines(self, request, obj=None):
        inlines = []
        for language in Language.objects.all():
            inline_class = type(
                f"DynamicPostLanguageInline{language.code}",
                (DynamicGeneralInformationLanguageInline,),
                {
                    "language_code": language.code,
                    "verbose_name": f"{language.name} data",
                }
            )
            inlines.append(inline_class)
        return tuple(inlines)

    def get_translation_field_value(self, translation):
        return translation.headline or "N/A"

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

