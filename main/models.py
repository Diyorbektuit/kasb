from django.db import models
from django.utils.text import slugify
import random
from django.utils.translation import gettext_lazy as _

from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(_("Created_at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated_at"), auto_now=True)

    objects = models.Manager()

    class Meta:
        abstract = True


class Category(BaseModel):
    name_uz = models.CharField(_("Name_uz"), max_length=512)
    name_eng = models.CharField(_("Name_eng"), max_length=512)
    name_ru = models.CharField(_("Name_ru"), max_length=512)
    order = models.PositiveIntegerField(_("Order"), default=1)

    def __str__(self):
        return self.name_eng


class Company(BaseModel):
    name_uz = models.CharField(_("Name_uz"), max_length=512)
    name_eng = models.CharField(_("Name_eng"), max_length=512)
    name_ru = models.CharField(_("Name_ru"), max_length=512)
    image = models.ImageField(upload_to='company_images')

    def __str__(self):
        return self.name_eng


class Country(BaseModel):
    name_uz = models.CharField(_("Name_uz"), max_length=512)
    name_eng = models.CharField(_("Name_eng"), max_length=512)
    name_ru = models.CharField(_("Name_ru"), max_length=512)

    def __str__(self):
        return self.name_eng


class Vacancy(BaseModel):
    title_uz = models.CharField(_("Title_uz"), max_length=512)
    title_eng = models.CharField(_("Title_eng"), max_length=512)
    title_ru = models.CharField(_("Title_ru"), max_length=512)
    description_uz = models.TextField(_("Description_uz"), null=True, blank=True)
    description_eng = models.TextField(_("Description_eng"), null=True, blank=True)
    description_ru = models.TextField(_("Description_ru"), null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="vacancies")
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name="vacancies")
    min_salary = models.IntegerField(_("Min_salary"))
    max_salary = models.IntegerField(_("Max_salary"))
    job_schedule = models.CharField(_("Job_schedule"), max_length=30, choices=
        [('full_time', _('Full-time')),
         ('part_time', _('Part-time')),
         ('shift', _('Shift')),
         ('flexible', _('Flexible'))])
    work_location = models.CharField(
        _("Job_location"),
        choices=[('office', _('Office')),
                 ('remote', _('Remote')),
                 ('hybrid', _('Hybrid'))],
        max_length=30
    )
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name='vacancies')
    city_uz = models.CharField(_("City_uz"), max_length=256)
    city_eng = models.CharField(_("City_eng"), max_length=256)
    city_ru = models.CharField(_("City_ru"), max_length=256)

    def __str__(self):
        return self.title_eng


class Application(BaseModel):
    fullname = models.CharField(_('Fullname'), max_length=256)
    phone_number = models.CharField(_('Phone_number'), max_length=512)
    email = models.EmailField(_('Email'))
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name='applications')
    vacancy = models.ForeignKey(Vacancy, on_delete=models.PROTECT, related_name='applications')
    extra_description = models.TextField(_('Extra_description'))

    def __str__(self):
        return self.fullname


class Post(BaseModel):
    title_uz = models.CharField(_('title_uz'), max_length=512)
    title_eng = models.CharField(_('title_eng'), max_length=512)
    title_ru = models.CharField(_('title_ru'), max_length=512)
    poster = models.ImageField(upload_to='post_images')
    short_description_uz = models.TextField(_('short_description_uz'))
    short_description_eng = models.TextField(_('short_description_eng'))
    short_description_ru = models.TextField(_('short_description_ru'))
    text_uz = RichTextUploadingField(_('text_uz'))
    text_eng = RichTextUploadingField(_('text_eng'))
    text_ru = RichTextUploadingField(_('text_ru'))
    slug = models.SlugField(_('slug'), unique=True)

    def unique_slugify(self):
        slug = slugify(self.title_eng)
        while Post.objects.filter(slug=slug).exists():
            slug = f"{slug}-{random.randint(100, 999)}"
        return slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.unique_slugify()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title_eng


class Form(BaseModel):
    fullname = models.CharField(_('fullname'), max_length=512)
    phone_number = models.CharField(_('Phone_number'), max_length=512)
    description = models.TextField(_("Description"))

    def __str__(self):
        return self.fullname
