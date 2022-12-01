from django.urls import path

from core.erp.views.alerts.views import AlertsSessionView
from core.erp.views.assistance.views import *
from core.erp.views.category.views import *
from core.erp.views.city.views import *
from core.erp.views.client.views import *
from core.erp.views.company.views import CompanyUpdateView
from core.erp.views.condition.views import *
from core.erp.views.employee.views import *
from core.erp.views.event_type.views import *
from core.erp.views.events.views import *
from core.erp.views.headings.views import *
from core.erp.views.product.views import *
from core.erp.views.provider.views import *
from core.erp.views.purchase.views import *
from core.erp.views.salary.views import *
from core.erp.views.sale.views import *
from core.erp.views.shipping_route.views import *
from core.erp.views.size.views import *
from core.erp.views.tariff.views import *
from core.reports.views.sale_report.views import SalePackagesReportView, SaleProductsReportView
from core.reports.views.shipping_route_report.views import ShippingRouteReportView

urlpatterns = [
    # company
    path('company/update/', CompanyUpdateView.as_view(), name='company_update'),
    # city
    path('city/', CityListView.as_view(), name='city_list'),
    path('city/add/', CityCreateView.as_view(), name='city_create'),
    path('city/update/<int:pk>/', CityUpdateView.as_view(), name='city_update'),
    path('city/delete/<int:pk>/', CityDeleteView.as_view(), name='city_delete'),
    # size
    path('size/', SizeListView.as_view(), name='size_list'),
    path('size/add/', SizeCreateView.as_view(), name='size_create'),
    path('size/update/<int:pk>/', SizeUpdateView.as_view(), name='size_update'),
    path('size/delete/<int:pk>/', SizeDeleteView.as_view(), name='size_delete'),
    # tariff
    path('tariff/', TariffListView.as_view(), name='tariff_list'),
    path('tariff/add/', TariffCreateView.as_view(), name='tariff_create'),
    path('tariff/update/<int:pk>/', TariffUpdateView.as_view(), name='tariff_update'),
    path('tariff/delete/<int:pk>/', TariffDeleteView.as_view(), name='tariff_delete'),
    # condition
    path('condition/', ConditionListView.as_view(), name='condition_list'),
    path('condition/add/', ConditionCreateView.as_view(), name='condition_create'),
    path('condition/update/<int:pk>/', ConditionUpdateView.as_view(), name='condition_update'),
    path('condition/delete/<int:pk>/', ConditionDeleteView.as_view(), name='condition_delete'),
    # client
    path('client/', ClientListView.as_view(), name='client_list'),
    path('client/add/', ClientCreateView.as_view(), name='client_create'),
    path('client/update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('client/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    # event_type
    path('event/type/', EventTypeListView.as_view(), name='event_type_list'),
    path('event/type/add/', EventTypeCreateView.as_view(), name='event_type_create'),
    path('event/type/update/<int:pk>/', EventTypeUpdateView.as_view(), name='event_type_update'),
    path('event/type/delete/<int:pk>/', EventTypeDeleteView.as_view(), name='event_type_delete'),
    # events
    path('events/', EventsListView.as_view(), name='events_list'),
    path('events/add/', EventsCreateView.as_view(), name='events_create'),
    path('events/update/<int:pk>/', EventsUpdateView.as_view(), name='events_update'),
    path('events/delete/<int:pk>/', EventsDeleteView.as_view(), name='events_delete'),
    # employee
    path('employee/', EmployeeListView.as_view(), name='employee_list'),
    path('employee/add/', EmployeeCreateView.as_view(), name='employee_create'),
    path('employee/update/<int:pk>/', EmployeeUpdateView.as_view(), name='employee_update'),
    path('employee/delete/<int:pk>/', EmployeeDeleteView.as_view(), name='employee_delete'),
    # headings
    path('headings/', HeadingsListView.as_view(), name='headings_list'),
    path('headings/add/', HeadingsCreateView.as_view(), name='headings_create'),
    path('headings/update/<int:pk>/', HeadingsUpdateView.as_view(), name='headings_update'),
    path('headings/delete/<int:pk>/', HeadingsDeleteView.as_view(), name='headings_delete'),
    # assistance
    path('assistance/', AssistanceListView.as_view(), name='assistance_list'),
    path('assistance/add/', AssistanceCreateView.as_view(), name='assistance_create'),
    path('assistance/update/<str:date_joined>/', AssistanceUpdateView.as_view(), name='assistance_create'),
    path('assistance/delete/<str:start_date>/<str:end_date>/', AssistanceDeleteView.as_view(), name='assistance_delete'),
    # salary
    path('salary/', SalaryListView.as_view(), name='salary_list'),
    path('salary/add/', SalaryCreateView.as_view(), name='salary_create'),
    path('salary/update/<int:year>/<int:month>/', SalaryUpdateView.as_view(), name='salary_update'),
    path('salary/delete/<int:year>/<int:month>/', SalaryDeleteView.as_view(), name='salary_delete'),
    path('salary/print/receipt/<int:pk>/', SalaryPrintReceiptView.as_view(), name='salary_print_receipt'),
    # provider
    path('provider/', ProviderListView.as_view(), name='provider_list'),
    path('provider/add/', ProviderCreateView.as_view(), name='provider_create'),
    path('provider/update/<int:pk>/', ProviderUpdateView.as_view(), name='provider_update'),
    path('provider/delete/<int:pk>/', ProviderDeleteView.as_view(), name='provider_delete'),
    # category
    path('category/', CategoryListView.as_view(), name='category_list'),
    path('category/add/', CategoryCreateView.as_view(), name='category_create'),
    path('category/update/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('category/delete/<int:pk>/', CategoryDeleteView.as_view(), name='category_delete'),
    # product
    path('product/', ProductListView.as_view(), name='product_list'),
    path('product/add/', ProductCreateView.as_view(), name='product_create'),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    # purchase
    path('purchase/', PurchaseListView.as_view(), name='purchase_list'),
    path('purchase/add/', PurchaseCreateView.as_view(), name='purchase_create'),
    path('purchase/delete/<int:pk>/', PurchaseDeleteView.as_view(), name='purchase_delete'),
    # sale
    path('sale/', SaleListView.as_view(), name='sale_list'),
    path('sale/add/', SaleCreateView.as_view(), name='sale_create'),
    path('sale/delete/<int:pk>/', SaleDeleteView.as_view(), name='sale_delete'),
    path('sale/print/invoice/<int:pk>/', SalePrintInvoiceView.as_view(), name='sale_print_invoice'),
    # shipping_route
    path('shipping/route/', ShippingRouteListView.as_view(), name='shipping_route_list'),
    path('shipping/route/add/<int:pk>/', ShippingRouteCreateView.as_view(), name='shipping_route_create'),
    path('shipping/route/print/invoice/<int:pk>/', SalePrintInvoiceView.as_view(), name='shipping_route_print_invoice'),
    path('shipping/route/delete/<int:pk>/', ShippingRouteDeleteView.as_view(), name='shipping_route_delete'),
    # packages
    path('packages/', SalePackagesReportView.as_view(title='Listado de Bodega de Paquetes'), name='packages'),
    path('parcel/service/', ShippingRouteListView.as_view(title='Listado de Servicios de Paquetería'), name='parcel_service'),
    path('parcel/alerts/', ShippingRouteReportView.as_view(title='Alertas de encomiendas'), name='parcel_alerts'),
    path('product/alerts/', ProductListView.as_view(title='Alerta de Productos de limpieza'), name='product_alerts'),
    path('service/warehouse/', SaleProductsReportView.as_view(title='Bodega de Servicios'), name='service_warehouse'),
    # alerts
    path('alerts/session/', AlertsSessionView.as_view(), name='alerts_session'),
]
