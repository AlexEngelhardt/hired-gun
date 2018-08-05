import datetime

from django.shortcuts import render
from django.db.models import F, Sum

from projects.models import Session

def index(request):
    
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
    return render(request, 'reports/index.html', context)

def get_total_earned(sessions):
    return sessions.aggregate(cash = Sum(F('units_worked') * F('project__rate')))['cash']

def report_month(request, year, month):
    sessions = Session.objects.filter(
        date__year=year,
        date__month=month
    )
    
    context = {
        'sessions': sessions,
        'year': year,
        'month': month,
        'total_earned': get_total_earned(sessions)
    }
    return render(request, 'reports/report.html', context)

def report_month_GET(request):
    year = request.GET.get('year')
    month = request.GET.get('month')

    ## This is redundant to what's in report_month()
    sessions = Session.objects.filter(
        date__year=year,
        date__month=month
    )
    
    context = {
        'sessions': sessions,
        'year': year,
        'month': month,
        'total_earned': get_total_earned(sessions)
    }
    return render(request, 'reports/report.html', context)

def report_POST(request):

    from_date = request.POST.get('from')
    to_date = request.POST.get('to')
    
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
    return render(request, 'reports/report.html', context)
