import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.erp.forms import EventType, EventTypeForm
from core.security.mixins import PermissionMixin


class EventTypeListView(PermissionMixin, ListView):
    model = EventType
    template_name = 'event_type/list.html'
    permission_required = 'view_event_type'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('event_type_create')
        context['title'] = 'Listado de Tipos de Eventos'
        return context


class EventTypeCreateView(PermissionMixin, CreateView):
    model = EventType
    template_name = 'event_type/create.html'
    form_class = EventTypeForm
    success_url = reverse_lazy('event_type_list')
    permission_required = 'add_event_type'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                data = self.get_form().save()
            elif action == 'validate_data':
                data = {'valid': True}
                queryset = EventType.objects.all()
                pattern = request.POST['pattern']
                parameter = request.POST['parameter'].strip()
                if pattern == 'name':
                    data['valid'] = not queryset.filter(name__iexact=parameter).exists()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de un Tipo de Evento'
        context['action'] = 'add'
        return context


class EventTypeUpdateView(PermissionMixin, UpdateView):
    model = EventType
    template_name = 'event_type/create.html'
    form_class = EventTypeForm
    success_url = reverse_lazy('event_type_list')
    permission_required = 'change_event_type'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'edit':
                data = self.get_form().save()
            elif action == 'validate_data':
                data = {'valid': True}
                queryset = EventType.objects.all().exclude(id=self.get_object().id)
                pattern = request.POST['pattern']
                parameter = request.POST['parameter'].strip()
                if pattern == 'name':
                    data['valid'] = not queryset.filter(name__iexact=parameter).exists()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de un Tipo de Evento'
        context['action'] = 'edit'
        return context


class EventTypeDeleteView(PermissionMixin, DeleteView):
    model = EventType
    template_name = 'event_type/delete.html'
    success_url = reverse_lazy('event_type_list')
    permission_required = 'delete_event_type'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.get_object().delete()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Notificación de eliminación'
        context['list_url'] = self.success_url
        return context
