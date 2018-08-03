import datetime

from django.shortcuts import render

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

def report_month(request, year, month):
    sessions = Session.objects.filter(
        date__year=year,
        date__month=month
    )
    context = {
        'sessions': sessions,
        'year': year,
        'month': month
    }
    return render(request, 'reports/report_month.html', context)

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
        'month': month
    }
    return render(request, 'reports/report_month.html', context)

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
        'to': to_date
    }
    return render(request, 'reports/report_custom.html', context)
