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


class Language(BaseModel):
    name = models.CharField(max_length=123)
    code = models.CharField(max_length=15, unique=True)
    icon = models.ImageField(upload_to='language_images/', null=True, blank=True)

    def __str__(self):
        return self.name


class Category(BaseModel):
    order = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)


class CategoryLanguage(BaseModel):
    language = models.ForeignKey(Language, on_delete=models.PROTECT, related_name='categories_languages')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='categories_languages')
    name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.language.name}, {self.name}"


class Company(BaseModel):
    image = models.ImageField(upload_to='company_images')

    def __str__(self):
        return str(self.id)


class CompanyLanguage(BaseModel):
    language = models.ForeignKey(Language, on_delete=models.PROTECT, related_name='companies_languages')
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='companies_languages')
    name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.language.name}, {self.name}"


class Country(BaseModel):
    icon = models.ImageField(upload_to='country-images/', null=True, blank=True)
    def __str__(self):
        return str(self.id)


class CountryLanguage(BaseModel):
    language = models.ForeignKey(Language, on_delete=models.PROTECT, related_name='countries_languages')
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name='countries_languages')
    name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.language.name}, {self.name}"


class Vacancy(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="vacancies")
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name="vacancies")
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name='vacancies')
    min_salary = models.IntegerField()
    max_salary = models.IntegerField()

    def __str__(self):
        return str(self.id)


class VacancyLanguage(BaseModel):
    language = models.ForeignKey(Language, on_delete=models.PROTECT, related_name='vacancies_languages')
    vacancy = models.ForeignKey(Vacancy, on_delete=models.PROTECT, related_name='vacancies_languages')
    title = models.CharField(max_length=512, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    job_schedule = models.CharField(max_length=512, null=True, blank=True)
    work_type = models.CharField(max_length=512, null=True, blank=True)
    city = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return f"{self.language.name}, {self.title}"


class Application(BaseModel):
    fullname = models.CharField(max_length=256)
    phone_number = models.CharField( max_length=512)
    email = models.EmailField()
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name='applications')
    vacancy = models.ForeignKey(Vacancy, on_delete=models.PROTECT, related_name='applications')
    extra_description = models.TextField()

    def __str__(self):
        return self.fullname


class Post(BaseModel):
    poster = models.ImageField(upload_to='post_images')

    def __str__(self):
        return str(self.id)


class PostLanguage(BaseModel):
    language = models.ForeignKey(Language, on_delete=models.PROTECT, related_name='posts_languages')
    post = models.ForeignKey(Post, on_delete=models.PROTECT, related_name='posts_languages')
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
