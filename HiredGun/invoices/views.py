from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic

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
    return render(request, 'invoices/invoice_edit.html', {'form': form})


@login_required
def edit_invoice(request, invoice_pk):

    invoice = get_object_or_404(Invoice, pk=invoice_pk)
    client_pk = invoice.client.pk
    
    # If the user already edited and is redirected here:
    if request.method == 'POST':
        form = InvoiceForm(request.user, client_pk, request.POST, instance=invoice)
        if form.is_valid():
            invoice = form.save(commit=False)
            # Here you could compute fields the user did not provide by hand,
            # e.g. a Session duration, or a 'last edited' timestamp
            invoice.save()
            return redirect('invoices:invoice-detail', pk=invoice.pk)

    # If he just clicked the edit button and will start now:
    else:
        form = InvoiceForm(request.user, client_pk, instance=invoice)
    return render(request, 'invoices/invoice_edit.html', {'form': form})


@login_required
def delete_invoice(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    invoice.delete()
    return redirect('invoices:invoice-list')

    
