import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView

from core.erp.forms import Tariff, TariffForm
from core.security.mixins import PermissionMixin


class TariffListView(PermissionMixin, TemplateView):
    template_name = 'tariff/list.html'
    permission_required = 'view_tariff'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                for i in Tariff.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('tariff_create')
        context['title'] = 'Listado de Cobertura y Tarifas'
        return context


class TariffCreateView(PermissionMixin, CreateView):
    model = Tariff
    template_name = 'tariff/create.html'
    form_class = TariffForm
    success_url = reverse_lazy('tariff_list')
    permission_required = 'add_tariff'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                data = self.get_form().save()
            elif action == 'validate_data':
                data = {'valid': True}
                queryset = Tariff.objects.all()
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
        context['title'] = 'Nuevo registro de una Tarifa'
        context['action'] = 'add'
        return context


class TariffUpdateView(PermissionMixin, UpdateView):
    model = Tariff
    template_name = 'tariff/create.html'
    form_class = TariffForm
    success_url = reverse_lazy('tariff_list')
    permission_required = 'change_tariff'

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
                queryset = Tariff.objects.all().exclude(id=self.get_object().id)
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
        context['title'] = 'Edición de una Tarifa'
        context['action'] = 'edit'
        return context


class TariffDeleteView(PermissionMixin, DeleteView):
    model = Tariff
    template_name = 'tariff/delete.html'
    success_url = reverse_lazy('tariff_list')
    permission_required = 'delete_tariff'

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
