from django.urls import include, path
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView)
from rest_framework.routers import DefaultRouter

from .views.user_view import UserRegistrationViewSet, UserViewSet, GroupViewSet
from .views.task_view import TaskViewSet
from .views.statistics_view import TaskStatisticsViewSet

v1_router = DefaultRouter()

v1_router.register('users', UserViewSet, basename='users')
v1_router.register(r'register', UserRegistrationViewSet, basename='user-register')
v1_router.register(r'tasks', TaskViewSet, basename='tasks')
v1_router.register(r'groups', GroupViewSet, basename='groups')
v1_router.register(r'tasks_statistics', TaskStatisticsViewSet, basename='tasks_statistics')

urlpatterns = [
    path("", include(v1_router.urls)),
    path("auth/", include('djoser.urls.jwt')),
]

urlpatterns += [
    path(
        'schema/',
        SpectacularAPIView.as_view(api_version='api/v1'),
        name='schema'
    ),
    path(
        'swagger/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui',
    ),
    path(
        'redoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc',
    ),
]
