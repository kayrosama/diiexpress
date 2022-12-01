import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.erp.forms import Size, SizeForm
from core.security.mixins import PermissionMixin


class SizeListView(PermissionMixin, ListView):
    model = Size
    template_name = 'size/list.html'
    permission_required = 'view_size'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('size_create')
        context['title'] = 'Listado de Tamaños'
        return context


class SizeCreateView(PermissionMixin, CreateView):
    model = Size
    template_name = 'size/create.html'
    form_class = SizeForm
    success_url = reverse_lazy('size_list')
    permission_required = 'add_size'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                data = self.get_form().save()
            elif action == 'validate_data':
                data = {'valid': True}
                queryset = Size.objects.all()
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
        context['title'] = 'Nuevo registro de un Tamaño'
        context['action'] = 'add'
        return context


class SizeUpdateView(PermissionMixin, UpdateView):
    model = Size
    template_name = 'size/create.html'
    form_class = SizeForm
    success_url = reverse_lazy('size_list')
    permission_required = 'change_size'

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
                queryset = Size.objects.all().exclude(id=self.get_object().id)
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
        context['title'] = 'Edición de un Tamaño'
        context['action'] = 'edit'
        return context


class SizeDeleteView(PermissionMixin, DeleteView):
    model = Size
    template_name = 'size/delete.html'
    success_url = reverse_lazy('size_list')
    permission_required = 'delete_size'

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
