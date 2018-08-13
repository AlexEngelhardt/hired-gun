from django import forms

from .models import Invoice
from projects.models import Client, Project

class InvoiceForm(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # TODO this very wrong
        
        client = forms.ModelChoiceField(
            queryset=Client.objects.filter(user=user),
            required=False,
            help_text='Leave empty to select all clients'
        )

        project = forms.ModelMultipleChoiceField(
            queryset = Project.objects.filter(client__user=user),
            required=False,
            help_text='Leave empty to select all projects'
        )
    
    class Meta:
        model = Invoice
        fields = '__all__'
