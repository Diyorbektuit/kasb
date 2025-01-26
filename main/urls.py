from django.urls import path
from main import views

urlpatterns = [
    path('languages/', views.LanguageListView.as_view()),
    path('vacancies/', views.VacancyListView.as_view()),
    path('application/', views.ApplicationCreateView.as_view()),
    path('posts/', views.PostListView.as_view()),
    path('posts/<int:pk>/', views.PostDetailView.as_view()),
    path('form/', views.FormCreateView.as_view()),
]