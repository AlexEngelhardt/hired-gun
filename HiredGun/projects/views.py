from django.views import generic
from django.shortcuts import render

from .models import Client, Project, Session

 
#### Index

def index(request):
    # https://docs.djangoproject.com/en/2.0/intro/tutorial03/
    context = None
    return render(request, 'projects/index.html', context)


#### Projects

class ProjectListView(generic.ListView):
    # the ListView generic view uses a default template called
    # <app name>/<model name>_list.html; we can use template_name to tell
    # ListView to use some existing "projects/index.html" template, for example.
    
    # template_name = 'projects/project_list.html'  # is default anyway
    context_object_name = 'projects'  # default is 'object_list'
    model = Project

class ProjectDetailView(generic.DetailView):
    model = Project
    # template_name = 'projects/project_detail.html'


#### Clients

class ClientListView(generic.ListView):
    context_object_name = 'clients'
    model = Client

class ClientDetailView(generic.DetailView):
    model = Client


#### Sessions

class SessionListView(generic.ListView):
    context_object_name = 'sessions'
    model = Session

class SessionDetailView(generic.DetailView):
    model = Session
