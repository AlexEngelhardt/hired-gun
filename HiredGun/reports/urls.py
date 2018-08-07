from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.unified_form, name='index'),
    path('earnings_report', views.earnings_report, name='total-earnings-report'),
]
