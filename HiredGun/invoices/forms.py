from django import forms

from .models import Invoice
from projects.models import Client, Project

class InvoiceForm(forms.ModelForm):

    def __init__(self, user, client_pk, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # TODO client should be done by get() instead of filter(), but that doesn't work somehow.
        self.fields['client'].queryset = Client.objects.filter(id=client_pk)
        
        # self.fields['project'].queryset = Project.objects.filter(client=client_pk)
        # self.fields['project'].required = False

    # project = forms.ModelMultipleChoiceField(
    #     queryset=Project.objects.all(),
    #     required=False
    # )

    class Meta:
        model = Invoice
        fields = '__all__'
        widgets = {
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
