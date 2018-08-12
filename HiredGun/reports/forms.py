from django import forms

from projects.models import Client, Project
from .helpers import get_initial_values

class ReportBaseForm(forms.Form):

    # TODO should this become a @classmethod, a @staticmethod?
    def giv(self):
        return self.initial_values

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

        client = forms.ModelChoiceField(
            queryset=Client.objects.filter(user=user),
            required=False,
            help_text='Leave empty to select all clients'
        )
        project = forms.ModelMultipleChoiceField(
            queryset=Project.objects.filter(client__user=user),
            required=False,
            help_text='Leave empty to select all projects'
        )
        
        self.initial_values = get_initial_values(self.user)
  

class ReportMonthlyForm(ReportBaseForm):

    # TODO to be very clean, I should have 'initial_values' as a field of ReportBaseForm, but
    # my OOP is not good enough for that to work

    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)

        self.year = forms.IntegerField(
            required=False,
            initial=self.initial_values['year_of_previous_month']
        )
        self.month = forms.IntegerField(
            required=False,
            initial=self.initial_values['previous_month']
        )


class ReportCustomForm(ReportBaseForm):

    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        
        self.from_date = forms.DateField(
            label='From',
            required=False,
            initial=self.initial_values['first_of_prev_month']
        )
        self.to_date = forms.DateField(
            required=False,
            label='To',
            initial=self.initial_values['last_of_prev_month']
        )
    
