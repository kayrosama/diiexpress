from datetime import datetime

from core.erp.models import Company, Product, TYPE_PRODUCT, ShippingRoute
from core.homepage.models import SocialNetworks
from core.security.models import Dashboard


def system_information(request):
    dashboard = Dashboard.objects.first()
    date_joined = datetime.now().date()
    parameters = {
        'dashboard': dashboard,
        'date_joined': datetime.now(),
        'company': Company.objects.first(),
        'social_networks': SocialNetworks.objects.filter(state=True).order_by('id'),
        'menu': 'hztbody.html' if dashboard is None else dashboard.get_template_from_layout(),
        'products': Product.objects.filter(stock__lte=4, type=TYPE_PRODUCT[0][0]).order_by('stock')[0:10],
        'shipping_routes': ShippingRoute.objects.filter(date_joined__year=date_joined.year, date_joined__month=date_joined.month, date_joined__day=date_joined.day).order_by('-id')[0:10]
    }
    return parameters
