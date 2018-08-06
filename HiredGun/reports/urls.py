from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.index, name='index'),
    path('unified_form', views.unified_form, name='unified-form'),
    path('earnings_report', views.earnings_report, name='total-earnings-report'),
]
