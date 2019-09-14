from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import SimpleRouter

from app import views


router = SimpleRouter()
router.register("messages", views.MessagesAPI, "messages")
router.register("auth/signup", views.RegistrationAPI, "signup")
router.register("auth/login", views.LoginAPI, "login")

api_patterns = [
    url(r"^", include(router.urls)),
]


schema_view = get_schema_view(
   openapi.Info(
      title="Hackathon API",
      default_version='v1.0',
      description="Hackathon API",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

api_patterns += [
   url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/v1.0/", include((api_patterns, "backend"), namespace="v1.0")),
    url(r"^files/(?P<file_>.*)$", views.files, name="files"),
]
