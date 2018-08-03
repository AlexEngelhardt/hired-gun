from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:year>/<int:month>/', views.report_month, name='report-month'),
    path('show_report_GET', views.report_month_GET, name='report-month-get'),
    path('show_report_POST', views.report_POST, name='report-post'),
]
