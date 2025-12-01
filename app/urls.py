# app/urls.py
from django.contrib import admin
from django.urls import path, include  # <--- Importe include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  # <--- Tudo vai para o app 'core'
]

# Isso permite servir os arquivos de áudio no modo DEBUG (Desenvolvimento)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)