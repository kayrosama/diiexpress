import json
import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, CreateView, DeleteView
from weasyprint import HTML, CSS

from config import settings
from core.erp.choices import TYPE_PRODUCT, TYPE_SALE
from core.erp.forms import Sale, SaleForm, PackageForm
from core.erp.models import Product, Tariff, SaleProducts, SalePackages, Company, ShippingRoute
from core.reports.forms import ReportForm
from core.security.mixins import PermissionMixin


class SaleListView(PermissionMixin, FormView):
    form_class = ReportForm
    template_name = 'sale/list.html'
    permission_required = 'view_sale'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']
                queryset = Sale.objects.filter()
                if len(start_date) and len(end_date):
                    queryset = queryset.filter(date_joined__range=[start_date, end_date])
                for i in queryset:
                    data.append(i.toJSON())
            elif action == 'search_detail_products':
                data = []
                for i in SaleProducts.objects.filter(sale_id=request.POST['id'], product__type=TYPE_PRODUCT[0][0]):
                    data.append(i.toJSON())
            elif action == 'search_detail_services':
                data = []
                for i in SaleProducts.objects.filter(sale_id=request.POST['id']).exclude(product__type=TYPE_PRODUCT[0][0]):
                    data.append(i.toJSON())
            elif action == 'search_detail_packages':
                data = []
                for i in SalePackages.objects.filter(sale_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('sale_create')
        context['title'] = 'Listado de Ventas de Servicios/Paqueteria'
        return context


class SaleCreateView(PermissionMixin, CreateView):
    model = Sale
    template_name = 'sale/create.html'
    form_class = SaleForm
    success_url = reverse_lazy('sale_list')
    permission_required = 'add_sale'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                with transaction.atomic():
                    sale = Sale()
                    sale.client_id = int(request.POST['client'])
                    sale.type = request.POST['type']
                    if sale.type == TYPE_SALE[0][0]:
                        sale.employee_id = int(request.POST['employee'])
                        sale.date_attention = request.POST['date_attention']
                    sale.date_joined = request.POST['date_joined']
                    sale.iva = float(Company.objects.first().iva) / 100
                    sale.save()
                    details = json.loads(request.POST['details'])
                    if sale.type == TYPE_SALE[0][0]:
                        for i in details['products']:
                            detail = SaleProducts()
                            detail.sale_id = sale.id
                            detail.product_id = int(i['id'])
                            detail.cant = int(i['cant'])
                            detail.price = float(i['pvp'])
                            detail.subtotal = detail.cant * float(detail.price)
                            detail.save()
                            detail.product.stock -= detail.cant
                            detail.product.save()
                        for i in details['services']:
                            detail = SaleProducts()
                            detail.sale_id = sale.id
                            detail.product_id = int(i['id'])
                            detail.cant = int(i['cant'])
                            detail.price = float(i['pvp'])
                            detail.subtotal = detail.cant * float(detail.price)
                            detail.save()
                    else:
                        for i in details['packages']:
                            detail = SalePackages()
                            detail.sale_id = sale.id
                            detail.description = i['description']
                            detail.tariff_id = int(i['tariff']['id'])
                            detail.condition_id = int(i['condition']['id'])
                            detail.size_id = int(i['size']['id'])
                            detail.peso = float(i['peso'])
                            detail.subtotal = float(i['amount'])
                            detail.save()
                        shipping_route = ShippingRoute()
                        shipping_route.sale_id = sale.id
                        shipping_route.comment = 'El paquete ya fue recibido y se esta gestionando para su envió.'
                        shipping_route.save()
                    sale.calculate_invoice()
                    sale.number = sale.generate_number()
                    sale.save()
            elif action == 'search_products':
                ids = json.loads(request.POST['ids'])
                data = []
                term = request.POST['term']
                queryset = Product.objects.filter(type=TYPE_PRODUCT[0][0], stock__gt=0).exclude(id__in=ids).order_by('name')
                if len(term):
                    queryset = queryset.filter(Q(name__icontains=term) | Q(code__icontains=term))
                    queryset = queryset[:10]
                for i in queryset:
                    item = i.toJSON()
                    item['value'] = i.get_full_name()
                    data.append(item)
            elif action == 'search_services':
                ids = json.loads(request.POST['ids'])
                data = []
                term = request.POST['term']
                queryset = Product.objects.filter().exclude(type=TYPE_PRODUCT[0][0]).exclude(id__in=ids).order_by('name')
                if len(term):
                    queryset = queryset.filter(Q(name__icontains=term) | Q(code__icontains=term))
                    queryset = queryset[:10]
                for i in queryset:
                    item = i.toJSON()
                    item['value'] = i.get_full_name()
                    data.append(item)
            elif action == 'search_tariff':
                data = []
                queryset = Tariff.objects.filter()
                term = request.POST['term']
                peso = request.POST['peso']
                if len(term):
                    queryset = queryset.filter(city__name__icontains=term)
                if len(peso):
                    peso = float(peso)
                    if peso > 0:
                        queryset = [q for q in queryset if peso >= q.minimum_weight and peso <= q.maximum_weight]
                for i in queryset[0:10]:
                    item = i.toJSON()
                    item['text'] = i.get_full_name()
                    item['data'] = i.toJSON()
                    data.append(item)
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de una Venta'
        context['action'] = 'add'
        context['frmPackage'] = PackageForm()
        return context


class SaleDeleteView(PermissionMixin, DeleteView):
    model = Sale
    template_name = 'sale/delete.html'
    success_url = reverse_lazy('sale_list')
    permission_required = 'delete_sale'

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


class SalePrintInvoiceView(LoginRequiredMixin, View):
    success_url = reverse_lazy('sale_list')

    def get_height_ticket(self):
        sale = Sale.objects.get(pk=self.kwargs['pk'])
        height = 450
        if sale.is_sale():
            increment = sale.saleproducts_set.all().count() * 10
        else:
            increment = sale.salepackages_set.all().count() * 10
        height += increment
        return round(height)

    def get(self, request, *args, **kwargs):
        try:
            sale = Sale.objects.get(pk=self.kwargs['pk'])
            context = {'sale': sale, 'company': Company.objects.first()}
            template = get_template('sale/ticket.html')
            context['height'] = self.get_height_ticket()
            html_template = template.render(context).encode(encoding="UTF-8")
            url_css = os.path.join(settings.BASE_DIR, 'static/lib/bootstrap-4.6.0/css/bootstrap.min.css')
            pdf_file = HTML(string=html_template, base_url=request.build_absolute_uri()).write_pdf(stylesheets=[CSS(url_css)], presentational_hints=True)
            return HttpResponse(pdf_file, content_type='application/pdf')
        except Exception as e:
            print(e)
            pass
        return HttpResponseRedirect(self.success_url)
