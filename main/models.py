from django.db import models
from django.utils.translation import gettext_lazy as _
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
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.fullname


class Application(BaseModel):
    fullname = models.CharField(max_length=256)
    gender = models.CharField(max_length=256, null=True, blank=True)
    marital_status = models.CharField(max_length=123, null=True, blank=True)
    birthday_data = models.DateTimeField(null=True, blank=True)
    region = models.CharField(max_length=123, null=True, blank=True)
    phone_number = models.CharField(max_length=512)
    email = models.EmailField()
    languages = models.CharField(max_length=1024, null=True, blank=True)
    country = models.CharField(max_length=256, null=True, blank=True)
    job_type = models.CharField(max_length=512, null=True, blank=True)
    experience = models.CharField(max_length=256, null=True, blank=True)
    level_of_education = models.CharField(max_length=1024, null=True, blank=True)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.PROTECT, related_name='applications', null=True, blank=True)

    def __str__(self):
        return self.fullname