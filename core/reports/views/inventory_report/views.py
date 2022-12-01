import json

from django.http import HttpResponse
from django.views.generic import FormView

from core.erp.choices import TYPE_PRODUCT
from core.erp.models import Product
from core.reports.forms import ReportForm
from core.security.mixins import ModuleMixin


class InventoryReportView(ModuleMixin, FormView):
    template_name = 'inventory_report/report.html'
    form_class = ReportForm

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'search_report':
                data = []
                product = request.POST['product']
                queryset = Product.objects.filter(type=TYPE_PRODUCT[0][0])
                if len(product):
                    queryset = queryset.filter(id=product)
                for i in queryset:
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Informe de inventario del servicio de limpieza'
        return context
