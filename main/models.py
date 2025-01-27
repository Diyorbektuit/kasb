from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor_uploader.fields import RichTextUploadingField

from settings.models import Language, Country
from vacancy.models import Vacancy


# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(_("Created_at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated_at"), auto_now=True)

    objects = models.Manager()

    class Meta:
        abstract = True


class Form(BaseModel):
    fullname = models.CharField(max_length=512)
    phone_number = models.CharField(max_length=512)
    description = models.TextField()

    def __str__(self):
        return self.fullname


class Application(BaseModel):
    fullname = models.CharField(max_length=256)
    phone_number = models.CharField( max_length=512)
    email = models.EmailField()
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name='applications')
    vacancy = models.ForeignKey(Vacancy, on_delete=models.PROTECT, related_name='applications')
    extra_description = models.TextField()

    def __str__(self):
        return self.fullname