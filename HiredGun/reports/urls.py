from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.index, name='index'),
    path('total_earnings_form', views.total_earnings_form, name='total-earnings-form'),
    path('per_client_form', views.per_client_form, name='per-client-form'),
    path('per_project_form', views.per_project_form, name='per-project-form'),
    
    path('earnings_report', views.earnings_report, name='total-earnings-report'),
]
