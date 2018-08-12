from django import forms

from .models import Invoice
from projects.models import Client, Project

class InvoiceForm(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['client'].queryset = Client.objects.filter(user=user)
        self.fields['project'].queryset = Project.objects.filter(client__user=user)
    
    class Meta:
        model = Invoice
        fields = '__all__'
