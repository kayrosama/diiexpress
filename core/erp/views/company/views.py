import json

from django.http import HttpResponse
from django.views.generic import UpdateView

from config import settings
from core.erp.forms import CompanyForm, Company
from core.security.mixins import PermissionMixin


class CompanyUpdateView(PermissionMixin, UpdateView):
    template_name = 'company/create.html'
    form_class = CompanyForm
    model = Company
    permission_required = 'view_company'
    success_url = settings.LOGIN_REDIRECT_URL

    def get_object(self, queryset=None):
        company = Company.objects.all()
        if company.exists():
            return company[0]
        return Company()

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            instance = self.get_object()
            if instance.pk is not None:
                form = CompanyForm(request.POST, request.FILES, instance=instance)
            else:
                form = CompanyForm(request.POST, request.FILES)
            activate_tax = 'activate_tax' in request.POST
            if not activate_tax:
                form.data._mutable = True
                form.data['iva'] = 0.00
            data = form.save()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Configuración de la Compañia'
        context['list_url'] = self.success_url
        return context
