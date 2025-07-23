from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title='My Product Management Dashboard',
        default_version='v1',
        description='',
        contact=openapi.Contact(email='oluwatimilehin.id@gmail.com'),
        license=openapi.License(name='MIT License')
    ),
    public=True
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/users/', include('api.users.urls', namespace='users')),
    path('api/v1/products/', include('api.products.urls', namespace='products')),

    #JWT
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    #SWAGGER DOCUMENTATION
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
