from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.views import generic
from django.apps import apps


def home_page(request):
    form = AuthenticationForm()
    return render(request, 'home.html', {'form': form})


class HomeView(generic.base.TemplateView):
    template_name = "home.html"

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
