import datetime

from django import forms

from .models import Invoice
from projects.models import Client, Project

class InvoiceForm(forms.ModelForm):
    # I don't actually need the 'user' in the __init__ or anywhere else right now.
    # But it would be nice (TODO) to only allow that users to access invoice/add/7 who actually
    # "owns" client with ID 7 :)
    
    def __init__(self, user, client_pk, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['project'].queryset = Project.objects.filter(client=client_pk)
        self.fields['project'].required = False
        
        # filter() returns a queryset, get() a single entity
        self.fields['client'].queryset = Client.objects.filter(id=client_pk)
        self.fields['client'].initial = Client.objects.get(id=client_pk)

        self.fields['invoice_no'].initial = Invoice.generate_invoice_number(user)

        self.fields['from_date'].initial = (datetime.date.today().replace(day=1) - datetime.timedelta(days=1)).replace(day=1)
        self.fields['to_date'].initial = datetime.date.today().replace(day=1) - datetime.timedelta(days=1)
        self.fields['invoice_date'].initial = datetime.date.today()

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
