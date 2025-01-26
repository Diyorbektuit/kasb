from django.contrib import admin
from django.contrib.auth.models import Group, User
from main import models

# Register your models here.
admin.site.unregister(Group)
admin.site.unregister(User)


# Helper class to add dynamic language fields
class MultiLanguageAdmin(admin.ModelAdmin):
    """
    Dinamik tillar uchun `list_display`ga ustunlarni qo'shish uchun yordamchi admin klass.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        languages = models.Language.objects.all()
        for language in languages:
            field_name = f'translation_{language.code}'
            self.list_display += (field_name,)

            # Dinamik metod yaratish
            def lang_translation(obj, lang_code=language.code):
                return self.get_translation(obj, lang_code)

            lang_translation.short_description = f'{language.name} Translation'
            setattr(self, field_name, lang_translation)

    def get_translation(self, obj, lang_code):
        """
        Tarjimani `language` va `obj` bo'yicha qaytaradi.
        """
        try:
            translation_model = self.translation_model
            translation = translation_model.objects.get(**{self.translation_fk_field: obj, 'language__code': lang_code})
            return self.get_translation_field_value(translation)
        except self.translation_model.DoesNotExist:
            return "N/A"

    def get_translation_field_value(self, translation):
        """
        Obyekt ichida qaysi qiymatni `list_display`da ko'rsatish.
        Default: `name` yoki `title`.
        """
        return getattr(translation, 'name', getattr(translation, 'title', "N/A"))


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


# Vacancy Admin
class VacancyLanguageInline(admin.TabularInline):
    model = models.VacancyLanguage
    extra = 0
    can_delete = False
    fields = ['language', 'title', 'description', 'job_schedule', 'work_type', 'city']
    readonly_fields = ['language']

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

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
class VacancyAdmin(MultiLanguageAdmin):
    list_display = ('id', 'category', 'company', 'country', 'min_salary', 'max_salary')
    translation_model = models.VacancyLanguage
    translation_fk_field = 'vacancy'
    inlines = (VacancyLanguageInline, ApplicationInline)

    def get_translation_field_value(self, translation):
        return translation.title or "N/A"


# Post Admin
class PostLanguageInline(admin.TabularInline):
    model = models.PostLanguage
    extra = 1
    fields = ['language', 'title', 'short_description', 'text']
    readonly_fields = ['language']

@admin.register(models.Post)
class PostAdmin(MultiLanguageAdmin):
    list_display = ('id', 'poster')
    translation_model = models.PostLanguage
    translation_fk_field = 'post'
    inlines = (PostLanguageInline, )

    def get_translation_field_value(self, translation):
        return translation.title or "N/A"



@admin.register(models.Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code')


@admin.register(models.Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'fullname', 'phone_number', 'email', 'country', 'vacancy')
    list_filter = ('country', 'vacancy')
    search_fields = ('fullname', 'phone_number', 'email')


@admin.register(models.Form)
class FormAdmin(admin.ModelAdmin):
    list_display = ('id', 'fullname', 'phone_number', 'description')
    search_fields = ('fullname', 'phone_number')

