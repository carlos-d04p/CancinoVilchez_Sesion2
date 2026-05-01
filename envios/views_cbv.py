# envios/views_cbv.py
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

from .models import Encomienda
from .forms import EncomiendaForm
from config.choices import EstadoEnvio

# 1. ListView: Lista paginada con filtros
class EncomiendaListView(LoginRequiredMixin, ListView):
    model = Encomienda
    template_name = 'envios/lista.html'
    context_object_name = 'encomiendas' # Nombre de la variable en el template
    paginate_by = 15
    ordering = ['-fecha_registro']
    
    def get_queryset(self):
        qs = Encomienda.objects.con_relaciones()
        estado = self.request.GET.get('estado')
        if estado:
            qs = qs.filter(estado=estado)
        return qs
        
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['estados'] = EstadoEnvio.choices
        return ctx

# 2. DetailView: Detalle de un registro
class EncomiendaDetailView(LoginRequiredMixin, DetailView):
    model = Encomienda
    template_name = 'envios/detalle.html'
    context_object_name = 'encomienda'
    
    def get_queryset(self):
        return Encomienda.objects.con_relaciones()
        
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['historial'] = self.object.historial.select_related('empleado')
        return ctx

# 3. CreateView: Formulario para crear una nueva encomienda
class EncomiendaCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Encomienda
    form_class = EncomiendaForm
    template_name = 'envios/form.html'
    success_message = 'Encomienda %(codigo)s creada correctamente.'
    
    def get_success_url(self):
        return reverse_lazy('encomienda_detalle', kwargs={'pk': self.object.pk})
        
    def form_valid(self, form):
        # Asignar el empleado antes de guardar
        form.instance.empleado_registro = self.request.user.empleado
        return super().form_valid(form)

# 4. UpdateView: Formulario para editar una encomienda
class EncomiendaUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Encomienda
    form_class = EncomiendaForm
    template_name = 'envios/form.html'
    success_message = 'Encomienda actualizada correctamente.'
    
    def get_success_url(self):
        return reverse_lazy('encomienda_detalle', kwargs={'pk': self.object.pk})