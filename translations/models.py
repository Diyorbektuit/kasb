from django.db import models

from settings.models import Language


# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    class Meta:
        abstract = True


class Group(BaseModel):
    name = models.CharField(max_length=256)
    sub_text = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return self.name


class Translation(BaseModel):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="translations")
    key = models.CharField(max_length=256)

    def __str__(self):
        return self.key

    class Meta:
        unique_together = ('group', 'key')

class TranslationLanguage(BaseModel):
    translation = models.ForeignKey(Translation, on_delete=models.CASCADE, related_name='languages')
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name="translations")
    value = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.language.name}, {self.id}"