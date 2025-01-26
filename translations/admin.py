from django.contrib import admin

from main.admin import MultiLanguageAdmin
from translations import models
# Register your models here.

# Vacancy Admin
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
    inlines = (TranslationLanguageInline, )
    list_filter = ('group', )
    search_fields = ('key', )


@admin.register(models.Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'sub_text']

