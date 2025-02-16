from django.contrib import admin
from django.contrib.auth.models import Group, User
from main import models
from posts.models import PostLanguage, Post
from settings.models import Language
from django.utils.html import format_html

# Register your models here.
admin.site.unregister(Group)
admin.site.unregister(User)


# Helper class to add dynamic language fields
class MultiLanguageAdmin(admin.ModelAdmin):
    translation_field = "value"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        languages = Language.objects.all()
        try:
            for language in languages:
                field_name = f'translation_{language.code}'
                self.list_display += (field_name,)

                def lang_translation(obj, lang_code=language.code):
                    return self.get_translation(obj, lang_code)

                lang_translation.short_description = f'{language.name} Translation'
                setattr(self, field_name, lang_translation)

        except Exception as e:
            print("Xatolik yuz berdi:", e)

    def get_translation(self, obj, lang_code):
        try:
            translation_model = self.translation_model
            translation = translation_model.objects.filter(**{self.translation_fk_field: obj, 'language__code': lang_code}).first()
            return self.get_translation_field_value(translation)
        except self.translation_model.DoesNotExist:
            return "N/A"

    def get_translation_field_value(self, translation):
        if not translation:
            return "N/A"
        return getattr(translation, self.translation_field, "N/A")


class DynamicPostLanguageInline(admin.StackedInline):
    model = PostLanguage
    extra = 0
    can_delete = False
    fields = ['language', 'title', 'short_description', 'text']
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

# Post Admin
class PostLanguageInline(admin.StackedInline):
    model = PostLanguage
    extra = 1
    fields = ['language', 'title', 'short_description', 'text']
    readonly_fields = ['language']

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj):
        return False

@admin.register(Post)
class PostAdmin(MultiLanguageAdmin):
    list_display = ('id', 'display_poster')
    translation_model = PostLanguage
    translation_field = 'title'
    translation_fk_field = 'post'
    inlines = (PostLanguageInline, )

    def get_inlines(self, request, obj=None):
        inlines = []
        for language in Language.objects.all():
            inline_class = type(
                f"DynamicPostLanguageInline{language.code}",
                (DynamicPostLanguageInline,),
                {
                    "language_code": language.code,
                    "verbose_name": f"{language.name} data",
                }
            )
            inlines.append(inline_class)
        return tuple(inlines)

    def get_translation_field_value(self, translation):
        return translation.title or "N/A"

    def display_poster(self, obj):
        if obj.poster:
            return format_html('<img src="{}" width="100" height="auto" />', obj.poster.url)
        return "No Poster"

    display_poster.short_description = 'Poster'

@admin.register(models.Form)
class FormAdmin(admin.ModelAdmin):
    list_display = ('id', 'fullname', 'phone_number', 'description')
    search_fields = ('fullname', 'phone_number')

