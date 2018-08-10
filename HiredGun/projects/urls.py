# The urls.py is not automatically created. You need to create this file
# by hand

from django.urls import path
from . import views


# app_names is for namespacing URLs in your template's html's {% url %} tags
# You'll have to use {% url 'projects:client-detail' ... %} now

app_name = 'projects'

# - The 'name' arguments are for removing hardcoded URLs in your templates:
# - Add a trailing slash to your paths, only then both ways (with and without slash) work in hrefs

urlpatterns = [
    # e.g. /projects/
    path('', views.index, name='index'),

    
    ## Clients
    
    path('clients/', views.ClientListView.as_view(), name='clients'),
    path('client/<int:pk>/', views.ClientDetailView.as_view(), name='client-detail'),
    
    path('clients/add', views.add_client, name='add-client'),
    path('clients/<int:pk>/edit', views.edit_client, name='edit-client'),
    path('clients/<int:pk>/delete', views.delete_client, name='delete-client'),

    
    ## Projects
    
    path('projects/', views.ProjectListView.as_view(), name='projects'),
    path('project/<int:pk>/', views.ProjectDetailView.as_view(), name='project-detail'),
    
    path('project/add', views.add_project, name='add-project'),
    path('project/<int:pk>/edit', views.edit_project, name='edit-project'),
    path('project/<int:pk>/delete', views.delete_project, name='delete-project'),

    
    ## Sessions
    
    path('sessions/', views.SessionListView.as_view(), name='sessions'),
    path('session/<int:pk>/', views.SessionDetailView.as_view(), name='session-detail'),

    path('session/add', views.add_session, name='add-session'),
    path('session/<int:pk>/edit', views.edit_session, name='edit-session'),
    path('session/<int:pk>/delete', views.delete_session, name='delete-session'),

]
