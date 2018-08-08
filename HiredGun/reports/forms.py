from django import forms

from projects.models import Client, Project
from .helpers import get_initial_values

class ReportBaseForm(forms.Form):

    # TODO should this become a @classmethod, a @staticmethod?
    def giv():
        return get_initial_values()

    client = forms.ModelChoiceField(
        queryset=Client.objects.all(),
        required=False,
        help_text='Leave empty to select all clients'
    )
    project = forms.ModelMultipleChoiceField(
        queryset=Project.objects.all(),
        required=False,
        help_text='Leave empty to select all projects'
    )
  

class ReportMonthlyForm(ReportBaseForm):

    # TODO to be very clean, I should have 'initial_values' as a field of ReportBaseForm, but
    # my OOP is not good enough for that to work

    initial_values = ReportBaseForm.giv()

    year = forms.IntegerField(
        required=False,
        initial=initial_values['year_of_previous_month']
    )
    month = forms.IntegerField(
        required=False,
        initial=initial_values['previous_month']
    )


class ReportCustomForm(ReportBaseForm):

    initial_values = ReportBaseForm.giv()

    from_date = forms.DateField(
        label='From',
        required=False,
        initial=initial_values['first_of_prev_month']
    )
    to_date = forms.DateField(
        required=False,
        label='To',
        initial=initial_values['last_of_prev_month']
    )
    
