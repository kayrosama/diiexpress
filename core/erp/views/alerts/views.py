import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import View


class AlertsSessionView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        try:
            alert = request.POST['alert']
            if alert in request.session:
                del request.session[alert]
        except:
            pass
        return HttpResponse(json.dumps({}), content_type='application/json')
