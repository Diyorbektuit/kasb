from django.contrib import admin
from django.contrib.auth.models import Group, User
from main import models
from posts.models import PostLanguage, Post
from settings.models import Language

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
        languages = Language.objects.all()
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
        Default: `value`, keyin `name`, keyin `title`.
        """
        return getattr(translation, 'value', getattr(translation, 'name', getattr(translation, 'title', "N/A")))


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
    list_display = ('id', 'poster')
    translation_model = PostLanguage
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


@admin.register(models.Form)
class FormAdmin(admin.ModelAdmin):
    list_display = ('id', 'fullname', 'phone_number', 'description')
    search_fields = ('fullname', 'phone_number')

