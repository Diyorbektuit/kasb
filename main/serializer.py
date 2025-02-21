from unicodedata import category

from rest_framework import serializers
from django.conf import settings

from main.models import Form, Application
from posts.models import Post
from settings.models import (Language, GeneralInformation, ApplicationLanguage, ApplicationExperience,
                             ApplicationJobType, Category, Company, Country, FAQ, Banner, CompanyLanguage)
from vacancy.models import Vacancy
from translations.models import Group


# Language serializer
class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = (
            'name',
            'code',
            'icon'
        )

# Vacancy serializer
class CompanyLanguageSerializerForVacancy(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        return obj.company.image.url

    class Meta:
        model = CompanyLanguage
        fields = (
            'name',
            'image'
        )


class VacancySerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    company = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    job_schedule = serializers.SerializerMethodField()
    work_type = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()

    def get_category(self, obj):
        code = self.context.get("language", None)
        if code is not None:
            category_language = obj.category.categories_languages.filter(language__code=code)
            if category_language.exists():
                return category_language.first().name
            return None
        return None

    def get_company(self, obj):
        code = self.context.get("language", None)
        if code is not None:
            company_language = obj.company.companies_languages.filter(language__code=code)
            if company_language.exists():
                return {
                    "image": f"{settings.HOST_URL}/media/{company_language.first().company.image}",
                    "name": company_language.first().name
                }
            return None
        return None

    def get_country(self, obj):
        code = self.context.get("language", None)
        if code is not None:
            country_language = obj.country.countries_languages.filter(language__code=code)
            if country_language.exists():
                return country_language.first().name
            return None
        return None

    def get_title(self, obj):
        code = self.context.get("language", None)
        if code is not None:
            vacancy_language = obj.vacancies_languages.filter(language__code=code)
            if vacancy_language.exists():
                return vacancy_language.first().title
            return None
        return None

    def get_description(self, obj):
        code = self.context.get("language", None)
        if code is not None:
            vacancy_language = obj.vacancies_languages.filter(language__code=code)
            if vacancy_language.exists():
                return vacancy_language.first().description
            return None
        return None

    def get_job_schedule(self, obj):
        code = self.context.get("language", None)
        if code is not None:
            vacancy_language = obj.vacancies_languages.filter(language__code=code)
            if vacancy_language.exists():
                return vacancy_language.first().job_schedule
            return None
        return None

    def get_work_type(self, obj):
        code = self.context.get("language", None)
        if code is not None:
            vacancy_language = obj.vacancies_languages.filter(language__code=code)
            if vacancy_language.exists():
                return vacancy_language.first().work_type
            return None
        return None

    def get_city(self, obj):
        code = self.context.get("language", None)
        if code is not None:
            vacancy_language = obj.vacancies_languages.filter(language__code=code)
            if vacancy_language.exists():
                return vacancy_language.first().city
            return None
        return None

    class Meta:
        model = Vacancy
        fields = [
            'id',
            'category',
            'company',
            'country',
            'min_salary',
            'max_salary',
            'title',
            'description',
            'job_schedule',
            'work_type',
            'city',
            'created_at'
        ]

# Application serializer
class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = (
            'fullname',
            'gender',
            'marital_status',
            'birthday_data',
            'region',
            'phone_number',
            'email',
            'languages',
            'country',
            'job_type',
            'experience',
            'level_of_education',
            'vacancy',
        )


    def to_representation(self, instance):
        return {
            'id': instance.id,
            'fullname': instance.fullname,
            'phone_number': instance.phone_number,
            'email': instance.email,
        }

# Post Serializers
class PostListSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    short_description = serializers.SerializerMethodField()

    def get_title(self, obj):
        code = self.context.get("language", None)
        if code is not None:
            post_language = obj.posts_languages.filter(language__code=code)
            if post_language.exists():
                return post_language.first().title
            return None
        return None

    def get_short_description(self, obj):
        code = self.context.get("language", None)
        if code is not None:
            post_language = obj.posts_languages.filter(language__code=code)
            if post_language.exists():
                return post_language.first().short_description
            return None
        return None

    def get_text(self, obj):
        code = self.context.get("language", None)
        if code is not None:
            post_language = obj.posts_languages.filter(language__code=code)
            if post_language.exists():
                return post_language.first().text
            return None
        return None

    class Meta:
        model = Post
        fields = (
            'id',
            'poster',
            'title',
            'short_description',
        )


class PostDetailSerializer(serializers.ModelSerializer):
    text = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    short_description = serializers.SerializerMethodField()
    next = serializers.SerializerMethodField()
    previous = serializers.SerializerMethodField()

    def get_next(self, obj):
        next_object = Post.objects.filter(id__gt=obj.id).order_by('id')
        if next_object.exists():
            return {
                'id': next_object.first().id,
                'title': self.get_title(next_object.first())
            }
        else:
            return None

    def get_previous(self, obj):
        previous_object = Post.objects.filter(id__lt=obj.id).order_by('id')
        if previous_object.exists():
            return {
                'id': previous_object.first().id,
                'title': self.get_title(previous_object.first())
            }
        else:
            return None

    def get_title(self, obj):
        code = self.context.get("language", None)
        if code is not None:
            post_language = obj.posts_languages.filter(language__code=code)
            if post_language.exists():
                return post_language.first().title
            return None
        return None

    def get_short_description(self, obj):
        code = self.context.get("language", None)
        if code is not None:
            post_language = obj.posts_languages.filter(language__code=code)
            if post_language.exists():
                return post_language.first().short_description
            return None
        return None

    def get_text(self, obj):
        code = self.context.get("language", None)
        if code is not None:
            post_language = obj.posts_languages.filter(language__code=code)
            if post_language.exists():
                return post_language.first().text.replace('src="/media/', f'src="{settings.HOST_URL}/media/')
            return None
        return None

    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'poster',
            'short_description',
            'text',
            'previous',
            'next'
        )


# Form serializer
class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = (
            'fullname',
            'phone_number',
            'description',
        )

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'fullname': instance.fullname,
            'phone_number': instance.phone_number,
            'description': instance.description,
        }


# GeneralInformation admin
class GeneralInformationSerializer(serializers.ModelSerializer):
    headline = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    opening_hours = serializers.SerializerMethodField()

    def get_headline(self, obj):
        code = self.context.get("language", None)
        if code is not None:
            information_language = obj.languages.filter(language__code=code)
            if information_language.exists():
                return information_language.first().headline
            return None
        return None

    def get_description(self, obj):
        code = self.context.get("language", None)
        if code is not None:
            information_language = obj.languages.filter(language__code=code)
            if information_language.exists():
                return information_language.first().description
            return None
        return None

    def get_address(self, obj):
        code = self.context.get("language", None)
        if code is not None:
            information_language = obj.languages.filter(language__code=code)
            if information_language.exists():
                return information_language.first().address
            return None
        return None

    def get_opening_hours(self, obj):
        code = self.context.get("language", None)
        if code is not None:
            information_language = obj.languages.filter(language__code=code)
            if information_language.exists():
                return information_language.first().opening_hours
            return None
        return None

    class Meta:
        model = GeneralInformation
        fields = (
            'email',
            'phone',
            'telegram',
            'instagram',
            'facebook',
            'youtube',
            'logo',
            'second_logo',
            'favicon',
            'headline',
            'description',
            'address',
            'opening_hours',
        )


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = (
            'name',
            'sub_text'
        )


class ApplicationLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationLanguage
        fields = (
            'value',
        )


class ApplicationExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationExperience
        fields = (
            'value',
        )

class ApplicationJobTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationJobType
        fields = (
            'value',
        )

class CategoryListSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = (
            'id',
            'name'
        )

    def get_name(self, obj):
        code = self.context.get("language", None)
        if code is not None:
            category_language = obj.categories_languages.filter(language__code=code)
            if category_language.exists():
                return category_language.first().name
            return None
        return None


class FAqListSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    class Meta:
        model = FAQ
        fields = (
            'id',
            'key',
            'value',
            'title',
        )

    def get_value(self, obj):
        code = self.context.get("language", None)
        if code is not None:
            faq_language = obj.faqs_languages.filter(language__code=code)
            if faq_language.exists():
                return faq_language.first().value
            return None
        return None


    def get_title(self, obj):
        code = self.context.get("language", None)
        if code is not None:
            faq_language = obj.faqs_languages.filter(language__code=code)
            if faq_language.exists():
                return faq_language.first().title
            return None
        return None


class CompanyListSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = (
            'id',
            'name'
        )

    def get_name(self, obj):
        code = self.context.get("language", None)
        if code is not None:
            company_language = obj.companies_languages.filter(language__code=code)
            if company_language.exists():
                return company_language.first().name
            return None
        return None


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = (
            'id',
            'image',
        )


class CountryListSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Country
        fields = (
            'id',
            'name'
        )

    def get_name(self, obj):
        code = self.context.get("language", None)
        if code is not None:
            countries_languages = obj.countries_languages.filter(language__code=code)
            if countries_languages.exists():
                return countries_languages.first().name
            return None
        return None