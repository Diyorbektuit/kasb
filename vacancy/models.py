from django.db import models

from settings.models import Category, Company, Country, Language


# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    class Meta:
        abstract = True


class Vacancy(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="vacancies")
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name="vacancies")
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name='vacancies')
    min_salary = models.IntegerField()
    max_salary = models.IntegerField()

    def __str__(self):
        return self.vacancies_languages.first().title if self.vacancies_languages.first().title is not None else str(self.id)


class VacancyLanguage(BaseModel):
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='vacancies_languages')
    vacancy = models.ForeignKey(Vacancy, on_delete=models.PROTECT, related_name='vacancies_languages')
    title = models.CharField(max_length=512, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    job_schedule = models.CharField(max_length=512, null=True, blank=True)
    work_type = models.CharField(max_length=512, null=True, blank=True)
    city = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return f"{self.language.name}, {self.title}"

