from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models


# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    class Meta:
        abstract = True

class Language(BaseModel):
    name = models.CharField(max_length=123)
    code = models.CharField(max_length=15, unique=True)
    icon = models.ImageField(upload_to='language_images/', null=True, blank=True)

    def __str__(self):
        return self.name


class Banner(BaseModel):
    image = models.ImageField(upload_to='banners/')

    def __str__(self):
        return str(self.id)


class GeneralInformation(BaseModel):
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=512, null=True, blank=True)
    telegram = models.CharField(max_length=512, null=True, blank=True)
    instagram = models.CharField(max_length=512, null=True, blank=True)
    facebook = models.CharField(max_length=512, null=True, blank=True)
    youtube = models.CharField(max_length=512, null=True, blank=True)
    logo = models.ImageField(upload_to='logo/', null=True, blank=True)
    second_logo = models.ImageField(upload_to='logo/', null=True, blank=True)
    favicon = models.ImageField(upload_to='favicon/', null=True, blank=True)

    def __str__(self):
        return self.phone if self.phone is not None else str(self.pk)


class GeneralInformationLanguage(BaseModel):
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='general_information')
    general_information = models.ForeignKey(GeneralInformation, on_delete=models.CASCADE, related_name="languages")
    headline = models.CharField(null=True, blank=True, max_length=512)
    description = RichTextUploadingField(null=True, blank=True)
    address = models.CharField(null=True, blank=True, max_length=512)
    opening_hours = models.CharField(null=True, blank=True, max_length=256)

    def __str__(self):
        return f"{self.language.name}, {self.general_information}"


class Category(BaseModel):
    order = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.categories_languages.first().name if self.categories_languages.first().name is not None else str(self.id)


class CategoryLanguage(BaseModel):
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='categories_languages')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='categories_languages')
    name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.language.name}, {self.name}"


class Company(BaseModel):
    image = models.ImageField(upload_to='company_images')

    def __str__(self):
        return self.companies_languages.first().name if self.companies_languages.first().name is not None else str(self.id)


class CompanyLanguage(BaseModel):
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='companies_languages')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='companies_languages')
    name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.language.name}, {self.name}"


class Country(BaseModel):
    icon = models.ImageField(upload_to='country-images/', null=True, blank=True)

    def __str__(self):
        return self.countries_languages.first().name if self.countries_languages.first().name is not None else str(self.id)


class CountryLanguage(BaseModel):
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='countries_languages')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='countries_languages')
    name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.language.name}, {self.name}"


class FAQ(BaseModel):
    key = models.CharField(max_length=2048)

    def __str__(self):
        return self.key


class FAQLanguage(BaseModel):
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='faqs_languages')
    faq = models.ForeignKey(FAQ, on_delete=models.CASCADE, related_name='faqs_languages')
    title = models.TextField(null=True, blank=True)
    value = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.language.name}, {self.value}"

    class Meta:
        unique_together = ('language', 'faq')


class ApplicationExperience(BaseModel):
    value = models.CharField(max_length=256)

    def __str__(self):
        return self.value


class ApplicationJobType(BaseModel):
    value = models.CharField(max_length=512)

    def __str__(self):
        return self.value


class ApplicationLanguage(BaseModel):
    value = models.CharField(max_length=512)

    def __str__(self):
        return self.value

