import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import FormView, DeleteView

from core.erp.choices import TYPE_SALE, STATUS_SENDING
from core.erp.forms import Sale, ShippingRouteForm, SalePackages, ShippingRoute
from core.reports.forms import ReportForm
from core.security.mixins import PermissionMixin


class ShippingRouteListView(PermissionMixin, FormView):
    form_class = ReportForm
    template_name = 'shipping_route/list.html'
    permission_required = 'view_shipping_route'
    title = 'Control de ruta de envío'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']
                queryset = Sale.objects.filter(type=TYPE_SALE[1][0])
                if len(start_date) and len(end_date):
                    queryset = queryset.filter(date_joined__range=[start_date, end_date])
                for i in queryset:
                    data.append(i.toJSON())
            elif action == 'search_detail_packages':
                data = []
                for i in SalePackages.objects.filter(sale_id=request.POST['id']):
                    data.append(i.toJSON())
            elif action == 'search_shipping_route':
                data = []
                for i in ShippingRoute.objects.filter(sale_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('shipping_route_create')
        context['title'] = self.title
        return context


class ShippingRouteCreateView(PermissionMixin, FormView):
    template_name = 'shipping_route/create.html'
    form_class = ShippingRouteForm
    success_url = reverse_lazy('shipping_route_list')
    permission_required = 'add_shipping_route'

    def load_states_in_select(self):
        items = []
        queryset = ShippingRoute.objects.filter(sale_id=self.kwargs['pk'])
        if queryset.filter(status=STATUS_SENDING[2][0]).exists():
            return items
        else:
            options = list(STATUS_SENDING)
            if queryset.exists():
                del options[0]
            else:
                options = options[0]
            for k, v in dict(options).items():
                items.append({'id': k, 'text': v})
        return items

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                shipping_route = ShippingRoute()
                shipping_route.sale_id = self.kwargs['pk']
                shipping_route.comment = request.POST['comment']
                shipping_route.status = request.POST['status']
                shipping_route.save()
            elif action == 'search_detail_packages':
                data = []
                for i in SalePackages.objects.filter(sale_id=self.kwargs['pk']):
                    data.append(i.toJSON())
            elif action == 'search_shipping_route':
                data = []
                queryset = ShippingRoute.objects.filter(sale_id=self.kwargs['pk']).order_by('id')
                for count, value in enumerate(queryset):
                    item = value.toJSON()
                    if count + 1 == queryset.count():
                        item['delete'] = True
                    data.append(item)
            elif action == 'remove_status_shipping_route':
                shipping_route = ShippingRoute.objects.get(pk=request.POST['id'])
                shipping_route.delete()
            elif action == 'load_states_in_select':
                data = self.load_states_in_select()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de un Control de ruta de envío'
        context['action'] = 'add'
        context['sale'] = Sale.objects.get(pk=self.kwargs['pk'])
        return context


class ShippingRouteDeleteView(PermissionMixin, DeleteView):
    model = Sale
    template_name = 'shipping_route/delete.html'
    success_url = reverse_lazy('shipping_route_list')
    permission_required = 'delete_shipping_route'

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
