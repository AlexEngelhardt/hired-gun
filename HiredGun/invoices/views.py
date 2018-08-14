from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Invoice
from .forms import InvoiceForm
from projects.models import Client, Project

# Create your views here.

@login_required
def index(request):
    clients = Client.objects.filter(user=request.user)
    context = {'clients': clients}
    return render(request, 'invoices/index.html', context)


class InvoiceListView(LoginRequiredMixin, generic.ListView):
    context_object_name = 'invoices'
    model = Invoice
    def get_queryset(self):
        # TODO still not user subsetted :D
        return Invoice.objects.all()

    
class InvoiceDetailView(LoginRequiredMixin, generic.DetailView):
    model = Invoice

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(client__user=self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = context['invoice'].project.all()
        return context

   
@login_required
def add_invoice(request, client_pk):

    if request.method == 'POST':
        form = InvoiceForm(request.user, client_pk, request.POST)
        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.save()
            return redirect('invoices:invoice-detail', pk=invoice.pk)
    else:
        form = InvoiceForm(request.user, client_pk)
    return render(request, 'invoices/invoice_form.html', {'form': form})


class InvoiceUpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    model = Invoice
    fields = '__all__'
    success_url = reverse_lazy('invoices:invoice-list')


class InvoiceDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Invoice
    success_url = reverse_lazy('invoices:invoice-list')


    
