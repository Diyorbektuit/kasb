from django.urls import path
from main import views

urlpatterns = [
    path('languages/', views.LanguageListView.as_view()),
    path('vacancies/', views.VacancyListView.as_view()),
    path('application/', views.ApplicationCreateView.as_view()),
    path('posts/', views.PostListView.as_view()),
    path('posts/<int:pk>/', views.PostDetailView.as_view()),
    path('form/', views.FormCreateView.as_view()),
    path('general-information/', views.GeneralInformationView.as_view()),
    path('translations/', views.TranslationView.as_view()),
    path('groups/', views.GroupListView.as_view()),
    path('application-job-types/', views.ApplicationJobTypeView.as_view()),
    path('application-languages/', views.ApplicationLanguageView.as_view()),
    path('application-experiences/', views.ApplicationExperienceView.as_view())
]