from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect

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

def remove_project(request, client_id):
    project = get_object_or_404(Project, pk=client_id)
    the_projects_client = project.client
    project.delete()
    
    return HttpResponseRedirect(reverse('projects:client-detail', args=(the_projects_client.id,)))
    
    
def add_project(request, client_id):
    try:
        client = Client.objects.get(pk=client_id)
    except Client.DoesNotExist:
        raise Http404("Client does not exist :(")

    # This is not pretty yet:
    # If end_date is not supplied, the <form> passes '' instead of None.
    # I need to replace it here.
    end_date = request.POST.get('end_date')
    if end_date == '':
        end_date = None
    
    new_proj = Project(
        name = request.POST.get('name', ''),
        client = client,
        rate = request.POST.get('rate', 0),
        rate_unit = request.POST.get('rate_unit', 'hr'),
        start_date = request.POST.get('start_date', None),
        end_date = end_date
    )

    new_proj.save()

    ## Do not do this!:
    # template = loader.get_template('projects/client_detail.html')
    # context = {
    #     'client': client,
    #     'message': 'Project added!',
    # }
    # return HttpResponse(template.render(context, request))

    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse('projects:client-detail', args=(client.id,)))
    # We are using the reverse() function in the HttpResponseRedirect constructor in
    # this example. This function helps avoid having to hardcode a URL in the view
    # function. It is given the name of the view that we want to pass control to and
    # the variable portion of the URL pattern that points to that view. In this
    # case, using the URLconf we set up in Tutorial 3, this reverse() call will return a string like
    # '/polls/3/results/'

    # TODO: But now I can't pass the "Project added!" message anymore :(


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
