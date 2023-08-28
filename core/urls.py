from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .views import  UserRegistrationView, UserLoginView, UserProfileView, SubjectListCreateAPI, SectionYearCreateAPI, ChapterTopicAPI, TopicCreateAPI, AssignmentCreateAPI, ResourceCreateAPI, SubjectDeleteAPI, PlanListCreateAPI, PlanTopicCreateAPI, PlanAssigmentCreateAPI, PlanResouceCreateAPI, ChapterDeleteAPI, PlanPdfView, AssignmentListViewAPI, ResourceListViewAPI, PlanDeleteAPI



urlpatterns = [
    path('auth/users/', UserRegistrationView.as_view()),
    path('auth/jwt/create/', UserLoginView.as_view()),
    path('auth/jwt/refresh/', jwt_views.TokenRefreshView.as_view()),
    path('auth/users/me/', UserProfileView.as_view()),
    path('subjects/', SubjectListCreateAPI.as_view()),
    path('subjects/<int:pk>/', SubjectDeleteAPI.as_view()),
    path('chapter/<int:pk>/', ChapterDeleteAPI.as_view()),
    path('sections/', SectionYearCreateAPI.as_view()),
    path('sections/<int:id>/chapters/', ChapterTopicAPI.as_view()),
    path('topics/', TopicCreateAPI.as_view()),
    path('assignments/', AssignmentCreateAPI.as_view()),
    path('resources/', ResourceCreateAPI.as_view()),
    path('sections/<int:id>/plan/', PlanListCreateAPI.as_view()),
    path('plan/<int:pk>/', PlanDeleteAPI.as_view()),
    path('plan/getpdf/<int:id>/', PlanPdfView.as_view()),
    path('plan/topic/', PlanTopicCreateAPI.as_view()),
    path('plan/assignment/', PlanAssigmentCreateAPI.as_view()),
    path('plan/resource/', PlanResouceCreateAPI.as_view()),
    path('assignment/<int:id>/', AssignmentListViewAPI.as_view()),
    path('resource/<int:id>/', ResourceListViewAPI.as_view()),
]
