
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # admin urls 
    path('admin/', admin.site.urls),
    
    # authentication urls
    path('api/v1/', include('djoser.urls')),
    path('api/v1/', include('djoser.urls.authtoken')),
    
    # apps urls 
    path('api/v1/', include('register.urls')),
    path('api/v1/', include('properties.urls')),
    
] +  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
