# envios/urls.py
from django.urls import path
from . import views

# (Nota: Quité lo de admin.site porque eso ya lo configuraste en config/urls.py 
# o en admin.py, aquí no hace falta y ensucia el código).

urlpatterns = [
    # Dashboard principal
    path('', views.dashboard, name='dashboard'),
    
    # Rutas de encomiendas (Usando tus vistas basadas en funciones)
    path('encomiendas/', views.encomienda_lista, name='encomienda_lista'),
    path('encomiendas/nueva/', views.encomienda_crear, name='encomienda_crear'),
    path('encomiendas/<int:pk>/', views.encomienda_detalle, name='encomienda_detalle'),
    path('encomiendas/<int:pk>/estado/', views.encomienda_cambiar_estado, name='encomienda_cambiar_estado'),
    
    # Si ya creaste la vista de editar en functions, sería esta:
    # path('encomiendas/<int:pk>/editar/', views.encomienda_editar, name='encomienda_editar'),
]