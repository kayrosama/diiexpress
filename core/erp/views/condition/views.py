import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.erp.forms import Condition, ConditionForm
from core.security.mixins import PermissionMixin


class ConditionListView(PermissionMixin, ListView):
    model = Condition
    template_name = 'condition/list.html'
    permission_required = 'view_condition'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('condition_create')
        context['title'] = 'Listado de Condiciones'
        return context


class ConditionCreateView(PermissionMixin, CreateView):
    model = Condition
    template_name = 'condition/create.html'
    form_class = ConditionForm
    success_url = reverse_lazy('condition_list')
    permission_required = 'add_condition'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                data = self.get_form().save()
            elif action == 'validate_data':
                data = {'valid': True}
                queryset = Condition.objects.all()
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
        context['title'] = 'Nuevo registro de una Condición'
        context['action'] = 'add'
        return context


class ConditionUpdateView(PermissionMixin, UpdateView):
    model = Condition
    template_name = 'condition/create.html'
    form_class = ConditionForm
    success_url = reverse_lazy('condition_list')
    permission_required = 'change_condition'

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
                queryset = Condition.objects.all().exclude(id=self.get_object().id)
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
        context['title'] = 'Edición de una Condición'
        context['action'] = 'edit'
        return context


class ConditionDeleteView(PermissionMixin, DeleteView):
    model = Condition
    template_name = 'condition/delete.html'
    success_url = reverse_lazy('condition_list')
    permission_required = 'delete_condition'

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
