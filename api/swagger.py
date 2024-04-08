from django.urls import path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from how_many.settings import (
    PROJECT_DESCRIPTION,
    PROJECT_NAME,
    PROJECT_VERSION,
)

schema_view = get_schema_view(
    openapi.Info(
        title=PROJECT_NAME,
        default_version=PROJECT_VERSION,
        description=PROJECT_DESCRIPTION,
        license=openapi.License(name='GPL-3.0-only'),
    ),
    public=True,
    permission_classes=(permissions.IsAuthenticatedOrReadOnly,),
)

urlpatterns = [
    re_path(
        r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json',
    ),
    path(
        'swagger/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui',
    ),
    path(
        'redoc/',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc',
    ),
]
