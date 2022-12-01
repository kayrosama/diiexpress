import json
from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, FloatField
from django.db.models.functions import Coalesce
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import requires_csrf_token
from django.views.generic import TemplateView

from core.erp.choices import TYPE_PRODUCT, MONTHS, TYPE_SALE
from core.erp.models import Sale, Client, Product, Category, ShippingRoute
from core.security.models import Dashboard


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'panel.html'

    def get(self, request, *args, **kwargs):
        request.user.set_group_session()
        request.session['module'] = None
        data = self.get_context_data()
        dashboard = Dashboard.objects.filter()
        if dashboard.exists():
            if dashboard[0].layout == 1:
                return render(request, 'vtcpanel.html', data)
        return render(request, 'hztpanel.html', data)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'get_graph_stock_products':
                data = []
                for i in Product.objects.filter(stock__gt=0).order_by('-stock')[0:10]:
                    data.append([i.name, i.stock])
            elif action == 'get_graph_sale_services_packages':
                data = []
                year = datetime.now().year
                rows = []
                queryset = Sale.objects.all()
                for i in MONTHS[1:]:
                    result = queryset.exclude(type=TYPE_SALE[1][0]).filter(date_joined__month=i[0], date_joined__year=year).aggregate(result=Coalesce(Sum('total'), 0.00, output_field=FloatField())).get('result')
                    rows.append(float(result))
                data.append({'name': 'Productos/Servicios', 'data': rows})
                rows = []
                for i in MONTHS[1:]:
                    result = queryset.exclude(type=TYPE_SALE[0][0]).filter(date_joined__month=i[0], date_joined__year=year).aggregate(result=Coalesce(Sum('total'), 0.00, output_field=FloatField())).get('result')
                    rows.append(float(result))
                data.append({'name': 'Paqueteria', 'data': rows})
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Panel de administración'
        context['sales'] = Sale.objects.filter().order_by('-id')[0:10]
        context['client'] = Client.objects.all().count()
        context['product'] = Product.objects.filter(type=TYPE_PRODUCT[0][0]).count()
        context['service'] = Product.objects.filter(type=TYPE_PRODUCT[1][0]).count()
        context['category'] = Category.objects.filter().count()
        context['current_date'] = datetime.now().date()
        return context


@requires_csrf_token
def error_404(request, exception):
    return render(request, '404.html', {})


@requires_csrf_token
def error_500(request, exception):
    return render(request, '500.html', {})
