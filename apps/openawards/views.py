from django.shortcuts import get_object_or_404
from django.views import generic
from django.apps import apps
from constance import config
from django.contrib.auth import get_user_model
import markdown


class HomeView(generic.base.TemplateView):
    template_name = "openawards/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['awards'] = apps.get_model('openawards', 'Award').objects.all()
        context['works'] = apps.get_model('openawards', 'Work').objects.all()
        return context


class AwardDetailView(generic.DetailView):
    model = apps.get_model('openawards', 'Award')


class WorkDetailView(generic.DetailView):
    model = apps.get_model('openawards', 'Work')


class UserDetailView(generic.DetailView):
    model = apps.get_model('openawards', 'User')

    def get_object(self):
        return get_object_or_404(get_user_model(), username=self.kwargs.get('username', ''))


class PastAwardsListView(generic.ListView):
    model = apps.get_model('openawards', 'Award')


class WorksListView(generic.ListView):
    model = apps.get_model('openawards', 'Work')
    template_name = 'work_list.html'


class EtiquetteView(generic.base.TemplateView):
    template_name = "openawards/etiquette.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['etiquette'] = markdown.markdown(config.ETIQUETTE_TEXT)
        return context
