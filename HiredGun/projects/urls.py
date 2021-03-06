# The urls.py is not automatically created. You need to create this file
# by hand

from django.urls import path
from . import views


# app_names is for namespacing URLs in your template's html's {% url %} tags
# You'll have to use {% url 'projects:client-detail' ... %} now

app_name = 'projects'

# - The 'name' arguments are for removing hardcoded URLs in your templates:
# - Add a trailing slash to your paths, only then both ways (with and without
#   slash) work in hrefs

urlpatterns = [
    # e.g. /projects/
    path('', views.index, name='index'),


    # Clients

    path('clients/', views.ClientListView.as_view(), name='clients'),
    path('clients/csv', views.client_csv_export_view, name='clients-csv'),
    path('client/<int:pk>/', views.ClientDetailView.as_view(),
         name='client-detail'),

    path('clients/add', views.ClientCreateView.as_view(), name='add-client'),
    path('clients/<int:pk>/edit', views.ClientUpdateView.as_view(),
         name='edit-client'),
    path('clients/<int:pk>/delete', views.ClientDeleteView.as_view(),
         name='delete-client'),

    # Projects

    path('projects/', views.ProjectListView.as_view(), name='projects'),
    path('projects/csv', views.project_csv_export_view, name='projects-csv'),
    path('project/<int:pk>/', views.ProjectDetailView.as_view(),
         name='project-detail'),

    path('project/add', views.ProjectCreateView.as_view(), name='add-project'),
    path('project/<int:pk>/edit', views.ProjectUpdateView.as_view(),
         name='edit-project'),
    path('project/<int:pk>/delete', views.ProjectDeleteView.as_view(),
         name='delete-project'),

    # Sessions

    path('sessions/', views.SessionListView.as_view(), name='sessions'),
    path('sessions/csv', views.session_csv_export_view, name='session-csv'),
    path('session/<int:pk>/', views.SessionDetailView.as_view(),
         name='session-detail'),

    path('session/add', views.SessionCreateView.as_view(), name='add-session'),
    path('session/<int:pk>/edit', views.SessionUpdateView.as_view(),
         name='edit-session'),
    path('session/<int:pk>/delete', views.SessionDeleteView.as_view(),
         name='delete-session'),

    path('sessions/not_invoiced/', views.SessionsNotInvoicedView.as_view(),
         name='sessions-not-invoiced-list'),
]
