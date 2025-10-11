from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('',include('mainapp.urls')),
    path('admin/',include('adminapp.urls')),
    path('voter/',include('voterapp.urls')),

    
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
