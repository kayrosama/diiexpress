import json

from django.http import HttpResponse
from django.views.generic import TemplateView, FormView

from core.erp.models import Category, ShippingRoute
from core.homepage.forms import CommentsForm
from core.homepage.models import FrequentQuestions, Testimonials, Services, Team, Comments


class IndexView(FormView):
    template_name = 'mainpage/index.html'
    form_class = CommentsForm

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'send_comment':
                comments = Comments()
                comments.names = request.POST['names']
                comments.mobile = request.POST['mobile']
                comments.email = request.POST['email']
                comments.comment = request.POST['comment']
                comments.save()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['frequent_questions'] = FrequentQuestions.objects.filter(state=True)
        context['testimonials'] = Testimonials.objects.filter(state=True)
        context['services'] = Services.objects.filter(state=True).order_by('id')
        context['team'] = Team.objects.filter(state=True).order_by('id')
        context['categories'] = Category.objects.filter().order_by('id')
        context['initial'] = True
        return context


class TrackOrderView(TemplateView):
    template_name = 'mainpage/track_order.html'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search_shipping_route':
                data = []
                queryset = ShippingRoute.objects.filter(sale__number=request.POST['number'])
                for i in queryset:
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
