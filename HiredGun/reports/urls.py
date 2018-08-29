from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.create_report_form, name='index'),
    path('client/<int:pk>/', views.create_report_form, name='create-per-client-report'),
    path('earnings_report', views.earnings_report, name='total-earnings-report'),
    path('simple_plot/', views.simple_plot, name='simple-plot'),
]
