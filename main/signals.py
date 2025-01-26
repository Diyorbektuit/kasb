import json

from django.db.models.signals import post_save
from django.dispatch import receiver

from main import models


@receiver(post_save, sender=models.Language)
def create_category_languages(sender, instance, created, **kwargs):
    if created:
        categories = models.Category.objects.all()
        companies = models.Company.objects.all()
        countries = models.Country.objects.all()
        vacancies = models.Vacancy.objects.all()
        posts = models.Post.objects.all()
        for category in categories:
            models.CategoryLanguage.objects.create(
                language=instance,
                category=category,
            )

        for company in companies:
            models.CompanyLanguage.objects.create(
                language=instance,
                company=company,
            )

        for country in countries:
            models.CountryLanguage.objects.create(
                language=instance,
                country=country,
            )

        for vacancy in vacancies:
            models.VacancyLanguage.objects.create(
                language=instance,
                vacancy=vacancy,
            )

        for post in posts:
            models.PostLanguage.objects.create(
                language=instance,
                post=post,
            )


@receiver(post_save, sender=models.Category)
def create_category_languages_for_new_category(sender, instance, created, **kwargs):
    if created:
        languages = models.Language.objects.all()
        for language in languages:
            models.CategoryLanguage.objects.create(
                language=language,
                category=instance,
            )


@receiver(post_save, sender=models.Country)
def create_category_languages_for_new_category(sender, instance, created, **kwargs):
    if created:
        languages = models.Language.objects.all()
        for language in languages:
            models.CountryLanguage.objects.create(
                language=language,
                country=instance,
            )


@receiver(post_save, sender=models.Company)
def create_category_languages_for_new_category(sender, instance, created, **kwargs):
    if created:
        languages = models.Language.objects.all()
        for language in languages:
            models.CompanyLanguage.objects.create(
                language=language,
                company=instance,
            )


@receiver(post_save, sender=models.Vacancy)
def create_category_languages_for_new_category(sender, instance, created, **kwargs):
    if created:
        languages = models.Language.objects.all()
        for language in languages:
            models.VacancyLanguage.objects.create(
                language=language,
                vacancy=instance,
            )


@receiver(post_save, sender=models.Post)
def create_category_languages_for_new_category(sender, instance, created, **kwargs):
    if created:
        languages = models.Language.objects.all()
        for language in languages:
            models.PostLanguage.objects.create(
                language=language,
                post=instance,
            )