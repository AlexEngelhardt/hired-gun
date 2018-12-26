import csv
import datetime

from django.views import generic
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .forms import SideProjectForm, SideIncomeForm
from .models import SideProject, SideIncome


################################################################
# Index

def index(request):
    context = None
    return render(request, 'side_income/index.html', context)


################################################################
# Side Projects


class SideProjectListView(LoginRequiredMixin, generic.ListView):
    context_object_name = 'side_projects'
    model = SideProject

    def get_queryset(self):
        return SideProject.objects.filter(user=self.request.user)


class SideProjectDetailView(LoginRequiredMixin, generic.DetailView):
    model = SideProject
    context_object_name = 'side_project'

    def get_queryset(self):
        qs = super().get_queryset().filter(user=self.request.user)
        return qs


class SideProjectCreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = SideProject
    form_class = SideProjectForm
    success_url = reverse_lazy('side_income:side-projects')

    def form_valid(self, form):
        form.instance.user = self.request.user
        # omg h4x
        return super().form_valid(form)


class SideProjectUpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    model = SideProject
    form_class = SideProjectForm
    success_url = reverse_lazy('side_income:side-projects')


class SideProjectDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = SideProject
    success_url = reverse_lazy('side_income:side-projects')


################################################################
# Side Income


class SideIncomeListView(LoginRequiredMixin, generic.ListView):
    context_object_name = 'side_incomes'
    model = SideIncome

    def get_queryset(self):
        return SideIncome.objects.filter(side_project__user=self.request.user)


class SideIncomeDetailView(LoginRequiredMixin, generic.DetailView):
    model = SideIncome
    context_object_name = 'side_income'

    def get_queryset(self):
        qs = super().get_queryset().filter(
            side_project__user=self.request.user)
        return qs


class SideIncomeCreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = SideIncome
    form_class = SideIncomeForm
    success_url = reverse_lazy('side_income:side-incomes')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # this gets pushed as an argument into the __init__ method:
        kwargs['the_user'] = self.request.user
        return kwargs


class SideIncomeUpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    model = SideIncome
    form_class = SideIncomeForm
    success_url = reverse_lazy('side_income:side-incomes')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # this gets pushed as an argument into the __init__ method:
        kwargs['the_user'] = self.request.user
        return kwargs


class SideIncomeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = SideIncome
    success_url = reverse_lazy('side_income:side-incomes')
