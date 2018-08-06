import datetime

from django.shortcuts import render
from django.db.models import F, Sum

from projects.models import Session


#### Helper functions

def get_total_earned(sessions):
    return sessions.aggregate(cash = Sum(F('units_worked') * F('project__rate')))['cash']

def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)  # dirty, but works
    return next_month - datetime.timedelta(days=next_month.day)

def prepare_report(from_date, to_date, client_id=None, project_id=None):
    sessions = Session.objects.filter(
        date__gte=from_date,
        date__lte=to_date
    )
    context = {
        'sessions': sessions,
        'from': from_date,
        'to': to_date,
        'total_earned': get_total_earned(sessions)
    }
    return context

#### Views

def index(request):
    context = {}
    return render(request, 'reports/index.html', context)

def total_month(request):
    year = request.GET.get('year')
    month = request.GET.get('month')

    from_date = datetime.date(int(year), int(month), 1)
    to_date = last_day_of_month(from_date)

    context = prepare_report(from_date, to_date)
    
    return render(request, 'reports/report.html', context)

def total_custom(request):
    from_date = request.POST.get('from')
    to_date = request.POST.get('to')
    
    # Convert the dates from 'yyyy-mm-dd' string into a datetime object so
    #  Django prints it nicely and in your locale (e.g. "1. Juli 2018")
    from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d').date()
    to_date = datetime.datetime.strptime(to_date, '%Y-%m-%d').date()

    context = prepare_report(from_date, to_date)

    return render(request, 'reports/report.html', context)

def request_total_earnings_report(request):
    last_of_prev_month = datetime.date.today().replace(day=1) - datetime.timedelta(days=1)
    first_of_prev_month = last_of_prev_month.replace(day=1)
    previous_month = last_of_prev_month.month
    year_of_previous_month = last_of_prev_month.year

    context = {
        'previous_month': previous_month,
        'year_of_previous_month': year_of_previous_month,
        'first_of_prev_month': first_of_prev_month.strftime('%Y-%m-%d'),
        'last_of_prev_month': last_of_prev_month.strftime('%Y-%m-%d')
    }
    return render(request, 'reports/create_total_report.html', context)

def per_client(request):
    pass

def per_project(request):
    pass
