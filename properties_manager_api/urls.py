
# django
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path

from rest_framework import permissions

# drf
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
   # admin urls 
   path('admin/', admin.site.urls),
    
   # authentication urls
   path('api/v1/', include('djoser.urls')),
   path('api/v1/', include('djoser.urls.authtoken')),
    
   # apps urls 
   path('api/v1/', include('register.urls')),
   path('api/v1/', include('properties.urls')),
   path('api/v1/', include('candidates.urls')),
   # path('api/v1/', include('payments.urls')),
   
   # tickets module with django 
   path('tickets', include('tickets.urls')),
   
    
   # drf urls
    
   re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    
] +  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# A JSON view of your API specification at /swagger.json
# A YAML view of your API specification at /swagger.yaml
# A swagger-ui view of your API specification at /swagger/
# A ReDoc view of your API specification at /redoc/