from django.views import generic
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .forms import ClientForm, ProjectForm, SessionForm
from .models import Client, Project, Session


################################################################
#### Index

def index(request):
    context = None
    return render(request, 'projects/index.html', context)


################################################################
#### Clients


class ClientListView(LoginRequiredMixin, generic.ListView):
    # the ListView generic view uses a default template called
    # <app name>/<model name>_list.html; we can use template_name to tell
    # ListView to use some existing "projects/index.html" template, for example.
    
    # template_name = 'projects/project_list.html'  # is default anyway
    context_object_name = 'clients'  # default is 'object_list'
    model = Client

    def get_queryset(self):
        return Client.objects.filter(user=self.request.user)

    
class ClientDetailView(LoginRequiredMixin, generic.DetailView):
    model = Client
    # template_name = 'projects/client_detail.html'
    
    def get_queryset(self):
        # This method filters out clients that don't belong to the requesting user
        qs = super().get_queryset().filter(user=self.request.user)
        return qs

class ClientCreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Client
    form = ClientForm
    # fields = '__all__'
    # exclude = ('user', )
    success_url = reverse_lazy('projects:clients')

class ClientUpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    model = Client
    form = ClientForm
    fields = '__all__'
    success_url = reverse_lazy('projects:clients')
    
class ClientDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Client
    success_url = reverse_lazy('projects:clients')
    

################################################################
#### Projects


class ProjectListView(LoginRequiredMixin, generic.ListView):
    context_object_name = 'projects'
    model = Project
    def get_queryset(self):
        return Project.objects.filter(client__user=self.request.user)

    
class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    model = Project
    def get_queryset(self):
        qs = super().get_queryset().filter(client__user=self.request.user)
        return qs

class ProjectCreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Project
    form = ProjectForm
    fields = '__all__'
    success_url = reverse_lazy('projects:projects')

class ProjectUpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    model = Project
    form = ProjectForm
    fields = '__all__'
    success_url = reverse_lazy('projects:projects')
    
class ProjectDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Project
    success_url = reverse_lazy('projects:projects')


################################################################
#### Sessions


class SessionListView(LoginRequiredMixin, generic.ListView):
    context_object_name = 'sessions'
    model = Session
    def get_queryset(self):
        return Session.objects.filter(project__client__user=self.request.user)

    
class SessionDetailView(LoginRequiredMixin, generic.DetailView):
    model = Session
    def get_queryset(self):
        qs = super().get_queryset().filter(project__client__user=self.request.user)
        return qs


class SessionCreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Session
    form = SessionForm
    fields = '__all__'
    success_url = reverse_lazy('projects:sessions')


class SessionUpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    model = Session
    form = SessionForm
    fields = '__all__'
    success_url = reverse_lazy('projects:session-list')
    
class SessionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Session
    success_url = reverse_lazy('projects:sessions')

