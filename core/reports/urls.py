from django.urls import path

from .views.database_backups_report.views import DatabaseBackupsReportView
from .views.purchase_report.views import PurchaseReportView
from .views.salary_report.views import SalaryReportView
from .views.sale_report.views import SaleReportView, SaleProductsReportView, SalePackagesReportView
from .views.employee_report.views import EmployeeReportView
from .views.inventory_report.views import InventoryReportView
from .views.shipping_route_report.views import ShippingRouteReportView

urlpatterns = [
    path('sale/', SaleReportView.as_view(), name='sale_report'),
    path('sale/products/', SaleProductsReportView.as_view(), name='sale_products_report'),
    path('sale/packages/', SalePackagesReportView.as_view(), name='sale_packages_report'),
    path('parcel/service/packages/', SalePackagesReportView.as_view(title='Informe de inventario del servicio de paquetería'), name='parcel_service_packages'),
    path('employee/', EmployeeReportView.as_view(), name='employee_report'),
    path('purchase/', PurchaseReportView.as_view(), name='purchase_report'),
    path('database/backups/', DatabaseBackupsReportView.as_view(), name='database_backups_report'),
    path('salary/', SalaryReportView.as_view(), name='salary_report'),
    path('inventory/', InventoryReportView.as_view(), name='inventory_report'),
    path('shipping/route/', ShippingRouteReportView.as_view(), name='shipping_route_report'),
]
