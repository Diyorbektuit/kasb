from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from main import models, serializer, pagination

# Create your views here.
class VacancyListView(generics.ListAPIView):
    queryset = models.Vacancy.objects.all()
    serializer_class = serializer.VacancySerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('title_uz', 'title_eng', 'title_ru')
    filterset_fields = ('country', 'category')
    pagination_class = pagination.VacancyPagination


class ApplicationCreateView(generics.CreateAPIView):
    queryset = models.Application.objects.all()
    serializer_class = serializer.ApplicationSerializer


class PostListView(generics.ListAPIView):
    queryset = models.Post.objects.all()
    serializer_class = serializer.PostListSerializer
    pagination_class = pagination.VacancyPagination


class PostDetailView(generics.RetrieveAPIView):
    queryset = models.Post.objects.all()
    serializer_class = serializer.PostDetailSerializer
    lookup_field = 'slug'


class FormCreateView(generics.CreateAPIView):
    queryset = models.Form.objects.all()
    serializer_class = serializer.FormSerializer

