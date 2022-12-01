import json

from django.db.models import Sum, FloatField
from django.db.models.functions import Coalesce
from django.http import HttpResponse
from django.views.generic import FormView

from core.erp.models import Salary
from core.reports.forms import ReportForm
from core.security.mixins import ModuleMixin


class SalaryReportView(ModuleMixin, FormView):
    template_name = 'salary_report/report.html'
    form_class = ReportForm

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'search_report':
                data = []
                year = request.POST['year']
                month = request.POST['month']
                employee = request.POST['employee']
                queryset = Salary.objects.filter()
                if len(employee):
                    queryset = queryset.filter(employee_id=employee)
                if len(year) and len(month):
                    queryset = queryset.filter(year=year, month=month)
                for i in queryset:
                    data.append(i.toJSON())
                total = float(queryset.aggregate(result=Coalesce(Sum('total'), 0.00, output_field=FloatField())).get('result'))
                data.append({
                    'id': '---',
                    'employee': {'names': '---', 'rmu': '---'},
                    'salary_by_day': '---',
                    'days_work': '---',
                    'rmu_month': '---',
                    'ingress': '---',
                    'egress': '---',
                    'total': f'{total:.2f}'
                })
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Informe de Roles de Pago'
        return context
