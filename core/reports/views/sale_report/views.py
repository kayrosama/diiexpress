import json

from django.db.models import Sum, FloatField
from django.db.models.functions import Coalesce
from django.http import HttpResponse
from django.views.generic import FormView

from core.erp.choices import TYPE_SALE
from core.erp.models import SaleProducts, Sale, SalePackages
from core.reports.forms import ReportForm
from core.security.mixins import ModuleMixin


class SaleReportView(ModuleMixin, FormView):
    template_name = 'sale_report/report.html'
    form_class = ReportForm

    def get_form(self, form_class=None):
        form = ReportForm()
        options = [('', '--------------')]
        options.extend(list(TYPE_SALE))
        form.fields['type_sale'].choices = options
        return form

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'search_report':
                data = []
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']
                type = request.POST['type']
                queryset = Sale.objects.filter()
                if len(type):
                    queryset = queryset.filter(type=type)
                if len(start_date) and len(end_date):
                    queryset = queryset.filter(date_joined__range=[start_date, end_date])
                for i in queryset:
                    data.append(i.toJSON())
                total = float(queryset.aggregate(result=Coalesce(Sum('total'), 0.00, output_field=FloatField())).get('result'))
                data.append({
                    'number': '---',
                    'date_joined': '---',
                    'client': {'names': '---'},
                    'employee_date_attention': '---',
                    'type': {'name': '---'},
                    'subtotal': '---',
                    'total_iva': '---',
                    'total': f'{total:.2f}'
                })
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Informe de Ventas Realizadas'
        return context


class SaleProductsReportView(ModuleMixin, FormView):
    template_name = 'sale_products/report.html'
    form_class = ReportForm
    title = 'Informe de bodega del servicio de limpieza'

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'search_report':
                data = []
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']
                queryset = SaleProducts.objects.filter()
                if len(start_date) and len(end_date):
                    queryset = queryset.filter(sale__date_joined__range=[start_date, end_date])
                for i in queryset:
                    item = i.toJSON()
                    item['sale'] = i.sale.toJSON()
                    data.append(item)
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context


class SalePackagesReportView(ModuleMixin, FormView):
    template_name = 'sale_packages/report.html'
    form_class = ReportForm
    title = 'Informe de bodega del servicio de paquetería'

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'search_report':
                data = []
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']
                queryset = SalePackages.objects.filter()
                if len(start_date) and len(end_date):
                    queryset = queryset.filter(sale__date_joined__range=[start_date, end_date])
                for i in queryset:
                    item = i.toJSON()
                    item['sale'] = i.sale.toJSON()
                    data.append(item)
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context
