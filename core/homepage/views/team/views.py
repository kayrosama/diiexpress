import json

from django.db import transaction
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView

from core.homepage.forms import Team, TeamForm
from core.homepage.models import TeamDetail
from core.security.mixins import PermissionMixin


class TeamListView(PermissionMixin, TemplateView):
    template_name = 'team/list.html'
    permission_required = 'view_team'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                for i in Team.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('team_create')
        context['title'] = 'Listado de Equipos de Trabajo'
        return context


class TeamCreateView(PermissionMixin, CreateView):
    model = Team
    template_name = 'team/create.html'
    form_class = TeamForm
    success_url = reverse_lazy('team_list')
    permission_required = 'add_team'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                with transaction.atomic():
                    team = Team()
                    team.names = request.POST['names']
                    team.profession = request.POST['profession']
                    team.description = request.POST['description']
                    if 'image' in request.FILES:
                        team.image = request.FILES['image']
                    team.state = 'state' in request.POST
                    team.save()
                    for i in json.loads(request.POST['items']):
                        detail = TeamDetail()
                        detail.team_id = team.id
                        detail.icon = i['icon']
                        detail.url = i['url']
                        detail.save()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de un Equipo de Trabajo'
        context['action'] = 'add'
        context['detail'] = []
        return context


class TeamUpdateView(PermissionMixin, UpdateView):
    model = Team
    template_name = 'team/create.html'
    form_class = TeamForm
    success_url = reverse_lazy('team_list')
    permission_required = 'change_team'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_detail(self):
        data = []
        team = self.get_object()
        for i in team.teamdetail_set.all():
            data.append(i.toJSON())
        return json.dumps(data)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'edit':
                with transaction.atomic():
                    team = self.get_object()
                    team.names = request.POST['names']
                    team.profession = request.POST['profession']
                    team.description = request.POST['description']
                    if 'image-clear' in request.POST:
                        team.remove_image()
                        team.image = None
                    if 'image' in request.FILES:
                        team.image = request.FILES['image']
                    team.state = 'state' in request.POST
                    team.save()
                    team.teamdetail_set.all().delete()
                    for i in json.loads(request.POST['items']):
                        detail = TeamDetail()
                        detail.team_id = team.id
                        detail.icon = i['icon']
                        detail.url = i['url']
                        detail.save()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de un Equipo de Trabajo'
        context['action'] = 'edit'
        context['detail'] = self.get_detail()
        return context


class TeamDeleteView(PermissionMixin, DeleteView):
    model = Team
    template_name = 'team/delete.html'
    success_url = reverse_lazy('team_list')
    permission_required = 'delete_team'

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
