from django import forms

from .models import Client, Project, Session

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        
        ## Provide one of (fields, exclude):
        # fields = ('name', 'billing_address', 'invoice_email', 'payment_terms',)
        exclude = ('', )


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ('', )

        
class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        exclude = ('', )
