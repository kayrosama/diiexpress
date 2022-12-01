import json

from django.http import HttpResponse
from django.views.generic import FormView

from core.erp.choices import TYPE_SALE
from core.erp.models import ShippingRoute, Sale
from core.reports.forms import ReportForm
from core.security.mixins import ModuleMixin


class ShippingRouteReportView(ModuleMixin, FormView):
    template_name = 'shipping_route_report/report.html'
    form_class = ReportForm
    title = 'Informe de control de rutas de envío'

    def get_form(self, form_class=None):
        form = ReportForm()
        form.fields['sale'].queryset = Sale.objects.filter(type=TYPE_SALE[1][0])
        return form

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'search_report':
                data = []
                id = request.POST['sale']
                queryset = ShippingRoute.objects.filter()
                if len(id):
                    queryset = queryset.filter(sale_id=id)
                    for i in queryset:
                        data.append(i.toJSON())
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context
