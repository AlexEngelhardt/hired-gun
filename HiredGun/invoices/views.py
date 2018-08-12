from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Invoice
from .forms import InvoiceForm

# Create your views here.

def index(request):
    context = {}
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


@login_required    
def add_invoice(request):
    if request.method == 'POST':
        form = InvoiceForm(request.user, request.POST)
        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.save()
            return redirect('invoices:invoice-detail', pk=invoice.pk)
    else:
        form = InvoiceForm(request.user)
    return render(request, 'invoices/invoice_edit.html', {'form': form})


@login_required
def edit_invoice(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)

    # If the user already edited and is redirected here:
    if request.method == 'POST':
        form = InvoiceForm(request.user, request.POST, instance=invoice)
        if form.is_valid():
            invoice = form.save(commit=False)
            # Here you could compute fields the user did not provide by hand,
            # e.g. a Session duration, or a 'last edited' timestamp
            invoice.save()
            return redirect('invoices:invoice-detail', pk=invoice.pk)

    # If he just clicked the edit button and will start now:
    else:
        form = InvoiceForm(request.user, instance=invoice)
    return render(request, 'invoices/invoice_edit.html', {'form': form})


@login_required
def delete_invoice(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    invoice.delete()
    return redirect('invoices:invoice-list')

    
