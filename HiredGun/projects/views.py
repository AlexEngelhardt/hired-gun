import csv
import datetime

from django.views import generic
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .forms import ClientForm, ProjectForm, SessionForm
from .models import Client, Project, Session
from django.contrib.auth.models import User


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
    form_class = ClientForm
    success_url = reverse_lazy('projects:clients')

    def form_valid(self, form):
        form.instance.user = self.request.user
        # omg h4x
        return super().form_valid(form)

class ClientUpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    model = Client
    form_class = ClientForm
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
    form_class = ProjectForm
    success_url = reverse_lazy('projects:projects')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['the_user'] = self.request.user  # this gets pushed as an argument into the __init__ method
        return kwargs

class ProjectUpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy('projects:projects')

    # TODO it should be possible to unite the redundant code in ProjectCreateView and ProjectUpdateView
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['the_user'] = self.request.user  # this gets pushed as an argument into the __init__ method
        return kwargs
    
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

class SessionsNotInvoicedView(SessionListView):
    
    def get_queryset(self):
        return Session.objects.filter(project__client__user=self.request.user).filter(invoice__isnull=True)
    
class SessionDetailView(LoginRequiredMixin, generic.DetailView):
    model = Session
    def get_queryset(self):
        qs = super().get_queryset().filter(project__client__user=self.request.user)
        return qs


class SessionCreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Session
    form_class = SessionForm
    success_url = reverse_lazy('projects:sessions')

    initial = {
        'date': datetime.date.today()
    }
    
    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs(*args, **kwargs)
        kwargs['user'] = self.request.user
        return kwargs
    

class SessionUpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    model = Session
    form_class = SessionForm
    success_url = reverse_lazy('projects:sessions')
    
    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs(*args, **kwargs)
        kwargs['user'] = self.request.user
        return kwargs



class SessionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Session
    success_url = reverse_lazy('projects:sessions')


################################################################
#### CSV export views

def csv_export_view(model, request, queryset, filename="export"):
    """
    Helper function holding redundant code for the CSV exports of 
    Clients, Projects, Sessions
    model = Client, e.g.
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="' + filename + '"'

    writer = csv.writer(response)

    writer.writerow(model.get_csv_head())
  
    for guy in queryset:
        writer.writerow(guy.get_csv_line())

    return response


def client_csv_export_view(request):
    queryset = Client.objects.filter(user=request.user)
    return csv_export_view(Client, request, queryset, "clients.csv")


def project_csv_export_view(request):
    queryset = Project.objects.filter(client__user=request.user)
    return csv_export_view(Project, request, queryset, "projects.csv")


def session_csv_export_view(request):
    queryset = Session.objects.filter(project__client__user=request.user)
    return csv_export_view(Session, request, queryset, "sessions.csv")
