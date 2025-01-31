from django.contrib import admin

from main.admin import MultiLanguageAdmin
from settings.models import Language
from translations import models


# Register your models here.
class DynamicTranslationLanguageInline(admin.StackedInline):
    model = models.TranslationLanguage
    extra = 0
    can_delete = False
    fields = ['language', 'value']
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


class TranslationLanguageInline(admin.TabularInline):
    model = models.TranslationLanguage
    extra = 0
    can_delete = False
    fields = ['language', 'value']
    readonly_fields = ['language']

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(models.Translation)
class TranslationAdmin(MultiLanguageAdmin):
    list_display = ('id', 'key')
    translation_model = models.TranslationLanguage
    translation_fk_field = 'translation'
    list_editable = ('key', )
    inlines = (TranslationLanguageInline, )
    list_filter = ('group', )
    search_fields = ('key', )

    def get_inlines(self, request, obj=None):
        inlines = []
        for language in Language.objects.all():
            inline_class = type(
                f"DynamicPostLanguageInline{language.code}",
                (DynamicTranslationLanguageInline,),
                {
                    "language_code": language.code,
                    "verbose_name": f"{language.name} data",
                }
            )
            inlines.append(inline_class)
        return tuple(inlines)


@admin.register(models.Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'sub_text']

