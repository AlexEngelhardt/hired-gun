from django.urls import path
from . import views

app_name = 'invoices'

urlpatterns = [
    path('', views.index, name='index'),
    
    path('list/', views.InvoiceListView.as_view(), name='invoice-list'),
    path('invoice/<int:pk>/', views.InvoiceDetailView.as_view(), name='invoice-detail'),

    path('invoice/add', views.add_invoice, name='add-invoice'),
    path('invoice/<int:pk>/edit', views.edit_invoice, name='edit-invoice'),
    path('invoice/<int:pk>/delete', views.delete_invoice, name='delete-invoice'),
]
