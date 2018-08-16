from django import forms

from django.contrib.auth.models import User

from .models import Client, Project, Session

class ClientForm(forms.ModelForm):

    class Meta:
        model = Client

        ## Provide one of (fields, exclude):
        # fields = ('name', 'billing_address', 'invoice_email', 'payment_terms',)
        fields = '__all__'
        # exclude = ('user', )


class ProjectForm(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['client'].queryset = Client.objects.filter(user=user)
    
    
    class Meta:
        model = Project
        exclude = ('', )  # same as fields = '__all__'
        widgets = {
            'start_date': forms.DateInput(
                format="%Y-%m-%d",
                attrs={'type': 'date'}
            ),
            'end_date': forms.DateInput(
                format="%Y-%m-%d",
                attrs={'type': 'date'}
            )
        }


class SessionForm(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['project'].queryset = Project.objects.filter(client__user=user)

    class Meta:
        model = Session
        exclude = ('', )
        widgets = {
            'date': forms.DateInput(
                format="%Y-%m-%d",
                attrs={'type': 'date'}
            )
        }
