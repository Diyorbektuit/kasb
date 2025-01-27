from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from main import models, serializer, pagination
from posts.models import Post
from vacancy.models import Vacancy
from settings.models import GeneralInformation, Language
from translations.models import Translation, Group


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


class TranslationView(generics.ListAPIView):
    queryset = Translation.objects.all()
    serializer_class = serializer.TranslationsSerializer

    def get_queryset(self):
        group = self.request.query_params.get("group", None)

        group = Group.objects.filter(name=group)
        if group.exists():
            return self.queryset.filter(group=group.first())
        return self.queryset

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
            ),
            openapi.Parameter(
                'group',
                openapi.IN_QUERY,
                description="group nomini yozasiz",
                type=openapi.TYPE_STRING
            )
        ])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class GroupListView(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = serializer.GroupSerializer
