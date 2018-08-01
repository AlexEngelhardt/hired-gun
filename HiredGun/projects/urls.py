# The urls.py is not automatically created. You need to create this file
# by hand

from django.urls import path
from . import views

# app_names is for namespacing URLs in your template's html's {% url %} tags
# https://docs.djangoproject.com/en/2.0/intro/tutorial03/#namespacing-url-names
app_name = 'projects'

# - The 'name' arguments are e.g. for removing hardcoded URLs in your templates:
#   https://docs.djangoproject.com/en/2.0/intro/tutorial03/#removing-hardcoded-urls-in-templates
# - Add a trailing slash to your paths, only then both ways (with and without slash) work in hrefs
urlpatterns = [
    # e.g. /projects/
    path('', views.index, name='index'),

    ## Clients
    path('clients/', views.ClientListView.as_view(), name='clients'),
    path('client/<int:pk>/', views.ClientDetailView.as_view(), name='client-detail'),
    path('client/<int:client_id>/add_project', views.add_project, name='add-project'),
    
    ## Projects
    path('projects/', views.ProjectListView.as_view(), name='projects'),
    path('project/<int:pk>/', views.ProjectDetailView.as_view(), name='project-detail'),
    path('project/<int:client_id>/remove', views.remove_project, name='remove-project'),
    
    ## Sessions
    path('sessions/', views.SessionListView.as_view(), name='sessions'),
    path('session/<int:pk>/', views.SessionDetailView.as_view(), name='session-detail'),

]
