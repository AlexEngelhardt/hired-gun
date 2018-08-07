import datetime
import pandas as pd

from django.shortcuts import render
from django.db.models import F, Sum

from projects.models import Client, Project, Session
from .forms import ReportMonthlyForm, ReportCustomForm

# I must store this function externally to avoid circular dependencies
# (ImportError: cannot import name 'get_initial_values').
# Otherwise, views.py would import .forms, and forms.py would import a fct from views.py
from .helpers import get_initial_values

#### Helper functions


def get_total_earned(sessions):
    return sessions.aggregate(cash = Sum(F('units_worked') * F('project__rate')))['cash']


def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)  # dirty, but works
    return next_month - datetime.timedelta(days=next_month.day)


def prepare_report(from_date, to_date, client_id=None, project_id=None):
    """
    Filters all relevant sessions to create a report.
    Filters a time span with the from and to arguments.
    Optionally filters by client or project
    """
    sessions = Session.objects.filter(
        date__gte=from_date,
        date__lte=to_date
    )

    if client_id is not None:
        sessions = sessions.filter(
            project__client=client_id
        )
    if project_id is not None:
        sessions = sessions.filter(
            project=project_id
        )

    date_range = pd.date_range(from_date, to_date).date

    sessions_per_date = {today: sessions.filter(date=today) for today in date_range}

    context = {
        'sessions': sessions,  # obsolete if sessions_per_date will work
        'from': from_date,
        'to': to_date,
        'date_range': date_range,
        'sessions_per_date': sessions_per_date,
        'total_earned': get_total_earned(sessions),
    }

    if client_id is not None:
        context['client'] = Client.objects.get(pk=client_id)
        
    if project_id is not None:
        context['project'] = Project.objects.get(pk=project_id)
    
    return context




def build_from_and_to_date(request):
    if 'from' in request.GET:
        from_date = request.GET.get('from')
        to_date = request.GET.get('to')
        # Convert the dates from 'yyyy-mm-dd' string into a datetime object so
        #  Django prints it nicely and in your locale (e.g. "1. Juli 2018")
        from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d').date()
        to_date = datetime.datetime.strptime(to_date, '%Y-%m-%d').date()

    else:
        # this means we used the other, monthly, way of calling this view:
        year = request.GET.get('year')
        month = request.GET.get('month')

        from_date = datetime.date(int(year), int(month), 1)
        to_date = last_day_of_month(from_date)

    return [ from_date, to_date ]


#### Views


def unified_form(request):
    context = get_initial_values()
    context['projects'] = Project.objects.all()
    context['clients'] = Client.objects.all()
    context['monthly_form'] = ReportMonthlyForm()
    context['custom_form'] = ReportCustomForm()
    return render(request, 'reports/create_report.html', context)
    

def earnings_report(request):
    from_date, to_date = build_from_and_to_date(request)

    # I think these default to None if they're not submitted
    client_id = request.GET.get('client')
    project_id = request.GET.get('project')
    
    context = prepare_report(from_date, to_date, client_id, project_id)

    return render(request, 'reports/report.html', context)

