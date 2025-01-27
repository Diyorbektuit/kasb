from django.db.models.signals import post_save
from django.dispatch import receiver

from posts.models import Post, PostLanguage
from settings.models import (Country, Company, Category, CategoryLanguage, CompanyLanguage, CountryLanguage, Language ,
                             GeneralInformation, GeneralInformationLanguage)
from vacancy.models import Vacancy, VacancyLanguage
from translations.models import Translation, TranslationLanguage


@receiver(post_save, sender=Language)
def create_category_languages(sender, instance, created, **kwargs):
    if created:
        categories = Category.objects.all()
        companies = Company.objects.all()
        countries = Country.objects.all()
        vacancies = Vacancy.objects.all()
        posts = Post.objects.all()
        translations = Translation.objects.all()

        general_information = GeneralInformation.objects.first()
        if general_information:
            GeneralInformationLanguage.objects.create(
                language=instance,
                general_information=general_information
            )

        for translation in translations:
            TranslationLanguage.objects.create(
                language=instance,
                translation=translation,
            )


        for category in categories:
            CategoryLanguage.objects.create(
                language=instance,
                category=category,
            )

        for company in companies:
            CompanyLanguage.objects.create(
                language=instance,
                company=company,
            )

        for country in countries:
            CountryLanguage.objects.create(
                language=instance,
                country=country,
            )

        for vacancy in vacancies:
            VacancyLanguage.objects.create(
                language=instance,
                vacancy=vacancy,
            )

        for post in posts:
            PostLanguage.objects.create(
                language=instance,
                post=post,
            )


@receiver(post_save, sender=Category)
def create_category_languages_for_new_category(sender, instance, created, **kwargs):
    if created:
        languages = Language.objects.all()
        for language in languages:
            CategoryLanguage.objects.create(
                language=language,
                category=instance,
            )


@receiver(post_save, sender=Country)
def create_category_languages_for_new_category(sender, instance, created, **kwargs):
    if created:
        languages = Language.objects.all()
        for language in languages:
            CountryLanguage.objects.create(
                language=language,
                country=instance,
            )


@receiver(post_save, sender=Company)
def create_category_languages_for_new_category(sender, instance, created, **kwargs):
    if created:
        languages = Language.objects.all()
        for language in languages:
            CompanyLanguage.objects.create(
                language=language,
                company=instance,
            )


@receiver(post_save, sender=Vacancy)
def create_category_languages_for_new_category(sender, instance, created, **kwargs):
    if created:
        languages = Language.objects.all()
        for language in languages:
            VacancyLanguage.objects.create(
                language=language,
                vacancy=instance,
            )


@receiver(post_save, sender=Post)
def create_category_languages_for_new_category(sender, instance, created, **kwargs):
    if created:
        languages = Language.objects.all()
        for language in languages:
            PostLanguage.objects.create(
                language=language,
                post=instance,
            )


@receiver(post_save, sender=GeneralInformation)
def create_category_languages_for_new_category(sender, instance, created, **kwargs):
    if created:
        languages = Language.objects.all()
        for language in languages:
            GeneralInformationLanguage.objects.create(
                language=language,
                general_information=instance,
            )

@receiver(post_save, sender=Translation)
def create_category_languages_for_new_category(sender, instance, created, **kwargs):
    if created:
        languages = Language.objects.all()
        for language in languages:
            TranslationLanguage.objects.create(
                language=language,
                translation=instance,
            )