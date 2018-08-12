from django.views import generic
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
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


@login_required    
def add_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            # Here you could compute fields the user did not provide by hand,
            # e.g. a Session duration, or a 'last edited' timestamp
            client.save()
            return redirect('projects:client-detail', pk=client.pk)
    else:
        form = ClientForm(initial = {'user': request.user.pk})
    return render(request, 'projects/client_edit.html', {'form': form})


@login_required
def edit_client(request, pk):
    client = get_object_or_404(Client, pk=pk)

    # If the user already edited and is redirected here:
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            client = form.save(commit=False)
            # Here you could compute fields the user did not provide by hand,
            # e.g. a Session duration, or a 'last edited' timestamp
            client.save()
            return redirect('projects:client-detail', pk=client.pk)

    # If he just clicked the edit button and will start now:
    else:
        form = ClientForm(instance=client)
    return render(request, 'projects/client_edit.html', {'form': form})


@login_required
def delete_client(request, pk):
    client = get_object_or_404(Client, pk=pk)
    client.delete()
    return redirect('projects:clients')


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

@login_required    
def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.user, request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.save()
            return redirect('projects:project-detail', pk=project.pk)
    else:
        form = ProjectForm(request.user)
    return render(request, 'projects/project_edit.html', {'form': form})


@login_required    
def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.method == 'POST':
        form = ProjectForm(request.user, request.POST, instance=project)
        if form.is_valid():
            project = form.save(commit=False)
            project.save()
            return redirect('projects:project-detail', pk=project.pk)
    else:
        form = ProjectForm(request.user, instance=project)
    return render(request, 'projects/project_edit.html', {'form': form})


@login_required    
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project.delete()
    return redirect('projects:projects')


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


def add_session(request):
    if request.method == 'POST':
        form = SessionForm(request.user, request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.save()
            return redirect('projects:session-detail', pk=session.pk)
    else:
        form = SessionForm(request.user)
    return render(request, 'projects/session_edit.html', {'form': form})


def edit_session(request, pk):
    session = get_object_or_404(Session, pk=pk)

    if request.method == 'POST':
        form = SessionForm(request.user, request.POST, instance=session)
        if form.is_valid():
            session = form.save(commit=False)
            session.save()
            return redirect('projects:session-detail', pk=session.pk)
    else:
        form = SessionForm(request.user, instance=session)
    return render(request, 'projects/session_edit.html', {'form': form})


def delete_session(request, pk):
    session = get_object_or_404(Session, pk=pk)
    session.delete()
    return redirect('projects:sessions')
