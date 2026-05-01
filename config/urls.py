# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Importamos nuestras vistas de autenticación personalizadas
from envios import views_auth

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('envios.urls')),
    
    # Usamos nuestras vistas propias (Opción B)
    # Les agregamos 'accounts/' al inicio para que coincidan con settings.py
    path('accounts/login/', views_auth.login_view, name='login'),
    path('accounts/logout/', views_auth.logout_view, name='logout'),
    path('accounts/perfil/', views_auth.perfil_view, name='perfil'),
]

# Configuración para servir archivos estáticos en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)