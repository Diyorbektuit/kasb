from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor_uploader.fields import RichTextUploadingField

from settings.models import Language

# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(_("Created_at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated_at"), auto_now=True)

    objects = models.Manager()

    class Meta:
        abstract = True


class Post(BaseModel):
    poster = models.ImageField(upload_to='post_images')

    def __str__(self):
        return str(self.id)


class PostLanguage(BaseModel):
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='posts_languages')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='posts_languages')
    title = models.CharField(max_length=512, null=True, blank=True)
    short_description = models.TextField(null=True, blank=True)
    text = RichTextUploadingField(null=True, blank=True)

    def __str__(self):
        return f"{self.language.name}, {self.title}"


class Form(BaseModel):
    fullname = models.CharField(max_length=512)
    phone_number = models.CharField(max_length=512)
    description = models.TextField()

    def __str__(self):
        return self.fullname
