from rest_framework import serializers
from django.conf import settings

from main.models import Post, Form
from settings.models import Language, GeneralInformation
from vacancy.models import Vacancy, Application


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
                return company_language.first().name
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
            'phone_number',
            'email',
            'country',
            'vacancy',
            'extra_description'
        )


    def to_representation(self, instance):
        return {
            'id': instance.id,
            'fullname': instance.fullname,
            'phone_number': instance.phone_number,
            'email': instance.email,
            'extra_description': instance.extra_description,
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

