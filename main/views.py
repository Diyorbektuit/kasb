from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from rest_framework.response import Response

from main import models, serializer, pagination
from posts.models import Post
from vacancy.models import Vacancy
from settings.models import GeneralInformation, Language, ApplicationLanguage, ApplicationExperience, \
    ApplicationJobType, Company, Category, Country, FAQ, Banner
from translations.models import Group

from collections.abc import Iterable

def is_iterable(obj):
    return isinstance(obj, Iterable)


# Create your views here.
class LanguageListView(generics.ListAPIView):
    queryset = Language.objects.all()
    serializer_class = serializer.LanguageSerializer


class VacancyListView(generics.ListAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = serializer.VacancySerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('vacancies_languages__title',)
    filterset_fields = ('country', 'category')
    pagination_class = pagination.VacancyPagination

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["language"] = self.request.query_params.get("language", None)
        return context

    def get_queryset(self):
        max_price = self.request.query_params.get("max_price", None)
        min_price = self.request.query_params.get("min_price", None)
        filters = Q()
        if min_price not in (None, ''):
            try:
                min_price = float(min_price)
                filters &= Q(min_salary__gte=min_price)
            except ValueError:
                pass

        if max_price not in (None, ''):
            try:
                max_price = float(max_price)
                filters &= Q(max_salary__lte=max_price)
            except ValueError:
                pass

        return Vacancy.objects.filter(filters)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'language',
                openapi.IN_QUERY,
                description="language codeni yozasiz",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'min_price',
                openapi.IN_QUERY,
                description="min price",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'max_price',
                openapi.IN_QUERY,
                description="max price",
                type=openapi.TYPE_INTEGER
            )
        ])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ApplicationCreateView(generics.CreateAPIView):
    queryset = models.Application.objects.all()
    serializer_class = serializer.ApplicationSerializer


class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = serializer.PostListSerializer
    pagination_class = pagination.VacancyPagination

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["language"] = self.request.query_params.get("language", None)
        return context

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'language',
                openapi.IN_QUERY,
                description="language codeni yozasiz",
                type=openapi.TYPE_STRING
            )
        ])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class PostDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = serializer.PostDetailSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["language"] = self.request.query_params.get("language", None)
        return context

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'language',
                openapi.IN_QUERY,
                description="language codeni yozasiz",
                type=openapi.TYPE_STRING
            )
        ])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class FormCreateView(generics.CreateAPIView):
    queryset = models.Form.objects.all()
    serializer_class = serializer.FormSerializer


class GeneralInformationView(generics.RetrieveAPIView):
    queryset = GeneralInformation.objects.all()
    serializer_class = serializer.GeneralInformationSerializer

    def get_object(self):
        return self.queryset.first()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["language"] = self.request.query_params.get("language", None)
        return context

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'language',
                openapi.IN_QUERY,
                description="language codeni yozasiz",
                type=openapi.TYPE_STRING
            )
        ])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class TranslationView(APIView):
    def get_queryset(self):
        group = self.request.query_params.get("group", None)
        if group is None:
            return Group.objects.all()
        group = Group.objects.filter(name=group)
        if group.exists():
            return group.first()
        return Group.objects.all()

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'language',
                openapi.IN_QUERY,
                description="language codeni yozasiz",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'group',
                openapi.IN_QUERY,
                description="group nomini yozasiz",
                type=openapi.TYPE_STRING
            )
        ])
    def get(self, request, *args, **kwargs):
        language = self.request.query_params.get('language', None)
        if language is None or not Language.objects.filter(code=language).exists():
            return Response(data={"msg": "language must be set"}, status=status.HTTP_400_BAD_REQUEST)
        queryset = self.get_queryset()
        if is_iterable(queryset):
            group_data = {}
            for group in queryset:
                group_translations = dict()
                for translation in group.translations.all():
                    group_translations.update(
                        {f"{translation.key}": translation.languages.filter(language__code=language).first().value})
                group_data.update({f"{group.name}": group_translations})

            return Response(data=group_data)

        group_translations = dict()
        for translation in queryset.translations.all():
            group_translations.update(
                {f"{translation.key}": translation.languages.filter(language__code=language).first().value})

        return Response(data=group_translations)



class GroupListView(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = serializer.GroupSerializer


class ApplicationLanguageView(generics.ListAPIView):
    queryset = ApplicationLanguage.objects.all()
    serializer_class = serializer.ApplicationLanguageSerializer


class ApplicationExperienceView(generics.ListAPIView):
    queryset = ApplicationExperience.objects.all()
    serializer_class = serializer.ApplicationExperienceSerializer


class ApplicationJobTypeView(generics.ListAPIView):
    queryset = ApplicationJobType.objects.all()
    serializer_class = serializer.ApplicationJobTypeSerializer


class CompanyListView(generics.ListAPIView):
    queryset = Company.objects.all()
    serializer_class = serializer.CompanyListSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'language',
                openapi.IN_QUERY,
                description="language codeni yozasiz",
                type=openapi.TYPE_STRING
            )
        ])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["language"] = self.request.query_params.get("language", None)
        return context

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = serializer.CategoryListSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'language',
                openapi.IN_QUERY,
                description="language codeni yozasiz",
                type=openapi.TYPE_STRING
            )
        ])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["language"] = self.request.query_params.get("language", None)
        return context


class FAQListView(generics.ListAPIView):
    queryset = FAQ.objects.all()
    serializer_class = serializer.FAqListSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'language',
                openapi.IN_QUERY,
                description="language codeni yozasiz",
                type=openapi.TYPE_STRING
            )
        ])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["language"] = self.request.query_params.get("language", None)
        return context


class BannersListView(generics.ListAPIView):
    queryset = Banner.objects.all()
    serializer_class = serializer.BannerSerializer


class CountryListView(generics.ListAPIView):
    queryset = Country.objects.all()
    serializer_class = serializer.CountryListSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'language',
                openapi.IN_QUERY,
                description="language codeni yozasiz",
                type=openapi.TYPE_STRING
            )
        ])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["language"] = self.request.query_params.get("language", None)
        return context