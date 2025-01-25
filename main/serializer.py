from rest_framework import serializers
from django.conf import settings

from main import models


# Category serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['name_uz', 'name_eng', 'name_ru']


# Company serializer
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Company
        fields = ['name_uz', 'name_eng', 'name_ru', 'image']


# Country serializer
class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Country
        fields = ['name_uz', 'name_eng', 'name_ru']


# Vacancy serializer
class VacancySerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    company = CompanySerializer()
    country = CountrySerializer()

    class Meta:
        model = models.Vacancy
        fields = [
            'title_uz', 'title_eng', 'title_ru',
            'description_uz', 'description_eng', 'description_ru',
            'category', 'company', 'min_salary', 'max_salary',
            'job_schedule', 'work_location', 'country', 'city_uz',
            'city_eng', 'city_ru'
        ]

# Application serializer
class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Application
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
            'country': {
                'name_uz': instance.country.name_uz,
                'name_eng': instance.country.name_eng,
                'name_ru': instance.country.name_ru
            },
            'vacancy': {
                'title_uz': instance.vacancy.title_uz,
                'title_eng': instance.vacancy.title_eng,
                'title_ru': instance.vacancy.title_ru
            }
        }

# Post Serializers
class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Post
        fields = (
            'slug',
            'title_uz',
            'title_eng',
            'title_ru',
            'poster',
            'short_description_uz',
            'short_description_eng',
            'short_description_ru',
        )

class PostDetailSerializer(serializers.ModelSerializer):
    text_uz = serializers.SerializerMethodField()
    text_eng = serializers.SerializerMethodField()
    text_ru = serializers.SerializerMethodField()

    class Meta:
        model = models.Post
        fields = (
            'slug',
            'title_uz',
            'title_eng',
            'title_ru',
            'poster',
            'short_description_uz',
            'short_description_eng',
            'short_description_ru',
            'text_uz',
            'text_eng',
            'text_ru'
        )

    def get_text_uz(self, obj):
        return obj.text_uz.replace('src="/media/', f'src="{settings.HOST_URL}/media/')

    def get_text_eng(self, obj):
        return obj.text_eng.replace('src="/media/', f'src="{settings.HOST_URL}/media/')

    def get_text_ru(self, obj):
        return obj.text_ru.replace('src="/media/', f'src="{settings.HOST_URL}/media/')

