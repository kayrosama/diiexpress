import json

from django.db import transaction
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import FormView, CreateView, UpdateView, DeleteView

from core.erp.forms import Events, EventsForm
from core.erp.models import Employee
from core.reports.forms import ReportForm
from core.security.mixins import PermissionMixin


class EventsListView(PermissionMixin, FormView):
    form_class = ReportForm
    template_name = 'events/list.html'
    permission_required = 'view_events'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']
                queryset = Events.objects.filter()
                if len(start_date) and len(end_date):
                    queryset = queryset.filter(start_date__range=[start_date, end_date])
                for i in queryset:
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('events_create')
        context['title'] = 'Listado de Eventos'
        return context


class EventsCreateView(PermissionMixin, CreateView):
    model = Events
    template_name = 'events/create.html'
    form_class = EventsForm
    success_url = reverse_lazy('events_list')
    permission_required = 'add_events'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                with transaction.atomic():
                    events = Events()
                    events.employee_id = int(request.POST['employee'])
                    events.event_type_id = int(request.POST['event_type'])
                    events.start_date = request.POST['start_date']
                    events.end_date = request.POST['end_date']
                    events.start_time = request.POST['start_time']
                    events.end_time = request.POST['end_time']
                    events.details = request.POST['details']
                    events.save()
            elif action == 'validate_data':
                data = {'valid': True}
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']
                start_time = request.POST['start_time']
                end_time = request.POST['end_time']
                event_type = request.POST['event_type']
                employee = request.POST['employee']
                if len(event_type) and len(employee):
                    data = {'valid': not Events.objects.filter(start_date=start_date, end_date=end_date, start_time=start_time, end_time=end_time, event_type_id=event_type, employee_id=employee).exclude(state=False).exists()}
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de un Evento'
        context['action'] = 'add'
        return context


class EventsUpdateView(PermissionMixin, UpdateView):
    model = Events
    template_name = 'events/create.html'
    form_class = EventsForm
    success_url = reverse_lazy('events_list')
    permission_required = 'change_events'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        instance = self.get_object()
        date_joined = f"{instance.start_date.strftime('%Y-%m-%d')} {instance.start_time.strftime('%H:%m')} - {instance.end_date.strftime('%Y-%m-%d')} {instance.end_time.strftime('%H:%m')}"
        form = EventsForm(instance=instance, initial={'date_joined': date_joined})
        form.fields['employee'].widget.attrs['disabled'] = True
        form.fields['employee'].queryset = Employee.objects.filter(id=instance.employee_id)
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'edit':
                with transaction.atomic():
                    events = self.get_object()
                    events.event_type_id = int(request.POST['event_type'])
                    events.start_date = request.POST['start_date']
                    events.end_date = request.POST['end_date']
                    events.start_time = request.POST['start_time']
                    events.end_time = request.POST['end_time']
                    events.details = request.POST['details']
                    events.save()
            elif action == 'validate_data':
                data = {'valid': True}
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']
                start_time = request.POST['start_time']
                end_time = request.POST['end_time']
                event_type = request.POST['event_type']
                employee = request.POST['employee']
                id = self.get_object().id
                if len(event_type) and len(employee):
                    data = {'valid': not Events.objects.filter(start_date=start_date, end_date=end_date, start_time=start_time, end_time=end_time, event_type_id=event_type, employee_id=employee).exclude(state=False).exclude(id=id).exists()}
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de un Evento'
        context['action'] = 'edit'
        return context


class EventsDeleteView(PermissionMixin, DeleteView):
    model = Events
    template_name = 'events/delete.html'
    success_url = reverse_lazy('events_list')
    permission_required = 'delete_events'

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
