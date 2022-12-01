import json

from django.http import HttpResponse
from django.views.generic import FormView

from core.erp.models import SalePackages
from core.reports.forms import ReportForm
from core.security.mixins import ModuleMixin


class PackagesListView(ModuleMixin, FormView):
    form_class = ReportForm
    template_name = 'packages/list.html'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
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
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Bodega de Paquetes'
        return context
