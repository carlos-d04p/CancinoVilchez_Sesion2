# envios/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse

from envios.forms import EncomiendaForm

from .models import Encomienda, Empleado, HistorialEstado
from clientes.models import Cliente
from rutas.models import Ruta
from config.choices import EstadoEnvio

from django.core.paginator import Paginator
from django.db.models import Q

# --- Vista del Dashboard ---
@login_required
def dashboard(request):
    """Vista principal del sistema con estadísticas"""
    hoy = timezone.now().date()
    context = {
        'total_activas': Encomienda.objects.activas().count(),
        'en_transito': Encomienda.objects.en_transito().count(),
        'con_retraso': Encomienda.objects.con_retraso().count(),
        'entregadas_hoy': Encomienda.objects.filter(
            estado=EstadoEnvio.ENTREGADO,
            fecha_entrega_real=hoy
        ).count(),
        'ultimas': Encomienda.objects.con_relaciones()[:5],
    }
    return render(request, 'envios/dashboard.html', context)

# --- Vista del Listado (con lógica básica de filtros y parámetros GET) ---
@login_required
def encomienda_lista(request):
    estado = request.GET.get('estado', '') 
    q = request.GET.get('q', '')
    
    qs = Encomienda.objects.con_relaciones()
    
    if estado:
        qs = qs.filter(estado=estado)
        
    if q:
        from django.db.models import Q
        qs = qs.filter(
            Q(codigo__icontains=q) |
            Q(remitente__apellidos__icontains=q) |
            Q(destinatario__apellidos__icontains=q)
        )
        
    return render(request, 'envios/lista.html', {'encomiendas': qs})

# --- Vista de Detalle ---
@login_required
def encomienda_detalle(request, pk):
    enc = get_object_or_404(Encomienda.objects.con_relaciones(), pk=pk)
    return render(request, 'envios/detalle.html', {'encomienda': enc})

# --- Vistas de Creación y Cambio de Estado (Stubs/Parciales hasta la pág 60) ---
@login_required
def encomienda_crear(request):
    if request.method == 'POST':
        form = EncomiendaForm(request.POST)
        if form.is_valid():
            enc = form.save(commit=False)
            enc.empleado_registro = request.user.empleado 
            enc.save()
            # MENSAJE DE ÉXITO:
            messages.success(request, f'Encomienda {enc.codigo} registrada correctamente.')
            return redirect('encomienda_detalle', pk=enc.pk)
        else:
            # MENSAJE DE ERROR:
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
    else:
        form = EncomiendaForm()
    
    return render(request, 'envios/form.html', {'form': form, 'titulo': 'Nueva Encomienda'})
@login_required
def encomienda_cambiar_estado(request, pk):
    return HttpResponse(f"Cambiar estado en construcción")

@login_required
def encomienda_lista(request):
    qs = Encomienda.objects.con_relaciones()
    
    # Filtros opcionales
    estado = request.GET.get('estado', '')
    q = request.GET.get('q', '')
    
    if estado:
        qs = qs.filter(estado=estado)
        
    if q:
        qs = qs.filter(
            Q(codigo__icontains=q) |
            Q(remitente__apellidos__icontains=q) |
            Q(destinatario__apellidos__icontains=q)
        )
        
    # Paginación
    paginator = Paginator(qs, 15) # Muestra 15 encomiendas por página
    page_number = request.GET.get('page', 1) # Obtiene el número de página de la URL
    encomiendas = paginator.get_page(page_number) # Obtiene solo los registros de esa página
    
    return render(request, 'envios/lista.html', {
        'encomiendas': encomiendas, 
        'estados': EstadoEnvio.choices,
        'estado_activo': estado,
        'q': q
    })

