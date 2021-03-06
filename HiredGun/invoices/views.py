from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Invoice
from .forms import InvoiceForm
from projects.models import Client, Project, Session
from projects.views import csv_export_view

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
        return Invoice.objects.filter(client__user=self.request.user)


def invoice_csv_export_view(request):
    queryset = Invoice.objects.filter(client__user=request.user)
    return csv_export_view(Invoice, request, queryset, "invoices.csv")


class InvoiceDetailView(LoginRequiredMixin, generic.DetailView):
    model = Invoice

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(client__user=self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # context['projects'] = context['invoice'].project.all()
        context['projects'] = self.object.get_implicit_projects()

        return context


class InvoicePrintView(InvoiceDetailView):
    template_name = 'invoices/invoice_print.html'


class InvoiceCreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Invoice
    form_class = InvoiceForm

    def get_form_kwargs(self):
        # this gets e.g. the POST data if you just created an invoice:
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['client_pk'] = self.kwargs['client_pk']
        return kwargs

    def get_success_url(self):
        return reverse_lazy('invoices:invoice-detail', args=[self.object.id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['client'] = Client.objects.get(id=self.kwargs['client_pk'])
        return context

    def form_valid(self, form):
        new_invoice = form.save(commit=False)
        # You must first save the invoice model, only then can you add its
        # PK to the sessions
        new_invoice.save()

        # Remove all existing session associations and add the newly submitted
        # ones:
        Session.objects.filter(invoice=new_invoice).update(invoice=None)
        # ^-- of course, in the CreateView this makes no sense, but I keep it
        # here to show these two classes can be easily consolidated (TODO) soon
        for sesh in form.cleaned_data['sessions']:
            new_invoice.session_set.add(sesh)

        return super().form_valid(form)


class InvoiceUpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    model = Invoice
    form_class = InvoiceForm
    success_url = reverse_lazy('invoices:invoice-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['client_pk'] = self.object.client.pk
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['client'] = Client.objects.get(id=self.object.client.pk)
        return context

    def form_valid(self, form):
        new_invoice = form.save(commit=False)
        # You must first save the invoice model, only then can you add its PK
        # to the sessions
        new_invoice.save()

        # Remove all existing session associations and add the newly submitted
        # ones:
        Session.objects.filter(invoice=new_invoice).update(invoice=None)
        for sesh in form.cleaned_data['sessions']:
            new_invoice.session_set.add(sesh)

        return super().form_valid(form)


class InvoiceDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Invoice
    success_url = reverse_lazy('invoices:invoice-list')
