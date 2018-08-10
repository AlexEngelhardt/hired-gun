from django import forms

from django.contrib.auth.models import User

from .models import Client, Project, Session


class ClientForm(forms.ModelForm):

    user = forms.ModelChoiceField(queryset=User.objects.all(),
                                  widget=forms.HiddenInput())
    
    class Meta:
        model = Client

        ## Provide one of (fields, exclude):
        # fields = ('name', 'billing_address', 'invoice_email', 'payment_terms',)
        fields = '__all__'



class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ('', )  # same as fields = '__all__'
        widgets = {
            'start_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
            'end_date': forms.DateInput(
                attrs={'type': 'date'}
            )
        }


class SessionForm(forms.ModelForm):
    
    class Meta:
        model = Session
        exclude = ('', )
        widgets = {
            'date': forms.DateInput(
                attrs={'type': 'date'}
            )
        }
