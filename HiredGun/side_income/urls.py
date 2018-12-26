from django.urls import path
from . import views


# app_names is for namespacing URLs in your template's html's {% url %} tags
# You'll have to use {% url 'projects:client-detail' ... %} now

app_name = 'side_income'

# - The 'name' arguments are for removing hardcoded URLs in your templates:
# - Add a trailing slash to your paths, only then both ways (with and without
#   slash) work in hrefs

urlpatterns = [
    # e.g. /side_income/
    path('', views.index, name='index'),

    # Side Projects

    path('side_projects/', views.SideProjectListView.as_view(),
         name='side-projects'),
    path('side_project/<int:pk>/', views.SideProjectDetailView.as_view(),
         name='side-project-detail'),
    path('side_project/add', views.SideProjectCreateView.as_view(),
         name='add-side-project'),
    path('side_project/<int:pk>/edit', views.SideProjectUpdateView.as_view(),
         name='edit-side-project'),
    path('side_project/<int:pk>/delete', views.SideProjectDeleteView.as_view(),
         name='delete-side-project'),

    # Side Income

    path('side_incomes/', views.SideIncomeListView.as_view(),
         name='side-incomes'),
    path('side_income/<int:pk>/', views.SideIncomeDetailView.as_view(),
         name='side-income-detail'),
    path('side_income/add', views.SideIncomeCreateView.as_view(),
         name='add-side-income'),
    path('side_income/<int:pk>/edit', views.SideIncomeUpdateView.as_view(),
         name='edit-side-income'),
    path('side_income/<int:pk>/delete', views.SideIncomeDeleteView.as_view(),
         name='delete-side-income'),
]
