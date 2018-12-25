import datetime

from django import forms
from django.db.models import Q

from .models import Invoice
from projects.models import Client, Project, Session


class InvoiceForm(forms.ModelForm):
    # I don't actually need the 'user' in the __init__ or anywhere else right
    # now. But it would be nice (TODO) to only allow that users to access
    # invoice/add/7 who actually "owns" client with ID 7 :)

    def __init__(self, user, client_pk, *args, **kwargs):
        super().__init__(*args, **kwargs)

        the_client = Client.objects.get(id=client_pk)

        # self.fields['project'].queryset = Project.objects.filter(
        #     client=client_pk)
        # self.fields['project'].required = False

        # filter() returns a queryset, get() a single entity
        self.fields['client'].queryset = Client.objects.filter(id=client_pk)
        self.fields['client'].initial = the_client

        self.fields['invoice_no'].initial = Invoice.generate_invoice_number(
            user)

        self.fields['from_date'].initial = (
            datetime.date.today().replace(day=1) - datetime.timedelta(days=1)
        ).replace(day=1)
        self.fields['to_date'].initial = datetime.date.today().replace(day=1) \
            - datetime.timedelta(days=1)
        self.fields['invoice_date'].initial = datetime.date.today()

        # TODO I'm reaaally not sure if I should set the model's (not the
        # form's!) client here.  But otherwise I wouldn't be able to
        # compute_due_date(), because it currently needs the client set
        self.instance.client = the_client
        self.fields['due_date'].initial = self.instance.compute_due_date()

        # Here I add a manual additional checkbox select for "all" sessions
        # within a certain time frame
        self.fields['sessions'] = forms.ModelMultipleChoiceField(
            queryset=Session.objects.filter(
                Q(invoice__isnull=True) | Q(invoice=self.instance),
                project__client=the_client
            ),
            # # default widget: forms.SelectMultiple
            # widget=forms.CheckboxSelectMultiple,
            required=False
        )
        self.fields['sessions'].initial = Session.objects.filter(
            invoice__isnull=False).filter(invoice=self.instance)

    class Meta:
        model = Invoice
        fields = '__all__'
        widgets = {
            'client': forms.Select(
                attrs={
                    'readonly': 'readonly'
                }
            ),
            'from_date': forms.DateInput(
                format="%Y-%m-%d",
                attrs={'type': 'date'}
            ),
            'to_date': forms.DateInput(
                format="%Y-%m-%d",
                attrs={'type': 'date'}
            ),
            'invoice_date': forms.DateInput(
                format="%Y-%m-%d",
                attrs={'type': 'date'}
            ),
            'paid_date': forms.DateInput(
                format="%Y-%m-%d",
                attrs={'type': 'date'}
            ),
            'due_date': forms.DateInput(
                format="%Y-%m-%d",
                attrs={'type': 'date'}
            )
        }
