"""
URL configuration for task_manager project.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from rest_framework.authtoken.views import obtain_auth_token
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Task Manager API",
      default_version='v1',
      description="""
      API для управления проектами и задачами.
      
      Основной функционал:
      - CRUD операции для проектов и задач
      - Фильтрация задач по статусу, дате, приоритету
      - Привязка задач к проектам и пользователям
      
      Аутентификация:
      - Bearer Token: передайте токен в заголовке Authorization: Bearer <token>
      - Basic Auth: для быстрого тестирования
      - Session Auth: для браузера
      """,
      contact=openapi.Contact(email="contact@taskmanager.local"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('tasks.urls')),
    
    # Authentication
    path('api/auth/token/', obtain_auth_token, name='api-token-auth'),
    
    # Swagger documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]

