from django.contrib import admin

from main.admin import MultiLanguageAdmin
from main.models import Application
from vacancy import models
from settings.models import Language

# Har bir til uchun alohida inline yaratish
class DynamicVacancyLanguageInline(admin.StackedInline):
    model = models.VacancyLanguage
    extra = 0
    can_delete = False
    fields = ['language', 'title', 'description', 'job_schedule', 'work_type', 'city']
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


# Vacancy Admin
class ApplicationInline(admin.TabularInline):
    model = Application
    extra = 0
    can_delete = False
    fields = ('id', 'fullname', 'phone_number', 'email', )
    readonly_fields = ('fullname', 'phone_number', 'email')

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(models.Vacancy)
class VacancyAdmin(MultiLanguageAdmin):
    list_display = ('id', 'category', 'company', 'country', 'min_salary', 'max_salary')
    translation_model = models.VacancyLanguage
    translation_fk_field = 'vacancy'
    translation_field = 'title'
    inlines = (ApplicationInline, )

    def get_inlines(self, request, obj=None):
        inlines = []
        for language in Language.objects.all():
            inline_class = type(
                f"DynamicVacancyLanguageInline_{language.code}",
                (DynamicVacancyLanguageInline,),
                {
                    "language_code": language.code,
                    "verbose_name": f"{language.name} data",
                }
            )
            inlines.append(inline_class)
        return tuple(inlines)

    def get_translation_field_value(self, translation):
        return translation.title or "N/A"


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'fullname', 'phone_number', 'email', 'country', 'vacancy')
    search_fields = ('fullname', 'phone_number', 'email')

