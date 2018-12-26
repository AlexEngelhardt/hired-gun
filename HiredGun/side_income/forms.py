from django import forms

from .models import SideProject, SideIncome


class SideProjectForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = SideProject
        exclude = ('user', )


class SideIncomeForm(forms.ModelForm):

    def __init__(self, the_user, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = SideIncome
        exclude = ('', )  # same as fields = '__all__'
        widgets = {
            'date': forms.DateInput(
                format="%Y-%m-%d",
                attrs={'type': 'date'}
            )
        }
