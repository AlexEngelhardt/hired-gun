from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.index, name='index'),
    path('total_month', views.total_month, name='total-month'),
    path('total_custom', views.total_custom, name='total-custom'),  # TODO unify these two into a total-earnings-report
    
    path('total_earnings', views.request_total_earnings_report, name='total-earnings'),
    path('per_client', views.per_client, name='per-client'),
    path('per_project', views.per_project, name='per-project'),
]
