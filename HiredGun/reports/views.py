import datetime
import pandas as pd

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from projects.models import Client, Project, Session
from side_income.models import SideProject, SideIncome

# I must store this function externally to avoid circular dependencies
# (ImportError: cannot import name 'get_initial_values').
# Otherwise, views.py would import .forms, and forms.py would import a fct
#  from views.py
from .helpers import get_initial_values


# Helper functions


def last_day_of_month(any_day):
    # dirty, but works:
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
    return next_month - datetime.timedelta(days=next_month.day)


def prepare_report(user, from_date, to_date,
                   show_which="worked",  # "worked", "invoiced", or "paid"
                   client_ids=[], project_ids=[]):
    """
    Filters all relevant sessions to create a report.
    Filters a time span with the from and to arguments.
    Optionally filters by client or project
    """

    if show_which == "worked":
        sessions = Session.objects.filter(
            project__client__user=user,
            date__gte=from_date,
            date__lte=to_date
        )
    elif show_which == "invoiced":
        sessions = Session.objects.filter(
            project__client__user=user,
            invoice__invoice_date__gte=from_date,
            invoice__invoice_date__lte=to_date
        )
    elif show_which == "paid":
        sessions = Session.objects.filter(
            project__client__user=user,
            invoice__paid_date__gte=from_date,
            invoice__paid_date__lte=to_date
        )
    else:
        raise ValueError("Invalid value for the 'show_which' argument "
                         "supplied")

    if client_ids != []:
        sessions = sessions.filter(
            project__client__in=client_ids
        )
    if project_ids != []:
        sessions = sessions.filter(
            project__in=project_ids
        )

    # Starting Python 3.6, the dict maintains order as inserted
    # When running this on a different computer with older Python,
    # the sessions_per_date was all jumbled-up.
    # https://stackoverflow.com/questions/1867861/dictionaries-how-to-keep-keys-values-in-same-order-as-declared
    date_range = pd.date_range(from_date, to_date).date
    sessions_per_date = {today: sessions.filter(date=today)
                         for today in date_range}

    total_earned = sum([sesh.get_money_earned() for sesh in sessions])

    context = {
        'sessions': sessions,  # obsolete if sessions_per_date will work
        'from': from_date,
        'to': to_date,
        'date_range': date_range,
        'sessions_per_date': sessions_per_date,
        'total_earned': total_earned,
    }

    if client_ids != []:
        context['clients'] = Client.objects.filter(pk__in=client_ids)

    if project_ids != []:
        context['projects'] = Project.objects.filter(pk__in=project_ids)

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

    return [from_date, to_date]


# (non-generic) Views
# Although you could use a django.views.generitc.edit.FormView for them, too.

@login_required
def create_report_form(request, pk=None):

    context = get_initial_values(request.user)
    context['projects'] = Project.objects.filter(client__user=request.user)
    context['clients'] = Client.objects.filter(user=request.user)

    if pk is not None:
        client = get_object_or_404(Client, pk=pk)
        context['client'] = client
        context['this_clients_projects'] = Project.objects.filter(
            client=client)

    return render(request, 'reports/create_report.html', context)


@login_required
def earnings_report(request):
    from_date, to_date = build_from_and_to_date(request)

    # getlist() returns either [] if the parameter was not submitted,
    # or a list of string IDs, like ['2', '3'].
    # /* get() would have returned None or 3, i.e. an int, if submitted */
    client_ids = request.GET.getlist('client')
    project_ids = request.GET.getlist('project')
    show_which = request.GET.get('show_which')

    context = prepare_report(request.user,
                             from_date, to_date,
                             show_which=show_which,
                             client_ids=client_ids, project_ids=project_ids)

    if request.GET.get('include_side_projects'):
        context['include_side_projects'] = True
        queryset = SideIncome.objects.filter(
            side_project__user=request.user,
            date__gte=from_date,
            date__lte=to_date
        )
        side_income_sum = queryset.aggregate(total=Sum('net_amount'))['total']
        if not side_income_sum:
            side_income_sum = 0
        context['side_income_sum'] = side_income_sum

    return render(request, 'reports/report.html', context)


################################################################
# Plots

from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import components
from bokeh.embed import file_html
from django.db.models.functions.datetime import ExtractMonth
import pandas as pd


def create_barplot(df):
    x = list(map(str, df.date))
    y = df.earned

    plot = figure(x_range=x, plot_height=300, plot_width=800,
                  title='Monthly earnings')
    plot.vbar(x=x, top=y, width=0.9)

    script, div = components(plot, CDN)
    return script, div


def create_ytdplot(df):
    x = df.date
    y = df['cumsum']

    plot = figure(plot_height=300, plot_width=800,
                  title='Cumulative earnings', x_axis_type='datetime')
    plot.line(x=x, y=y)

    script, div = components(plot, CDN)
    return script, div


@login_required
def plots(request):
    sessions = Session.objects.filter(
        project__client__user=request.user,
        date__year=datetime.datetime.today().year
    )
    cashies = list(
        map(lambda x: (x.date.month, x.date.year, x.get_money_earned()),
            sessions)
    )
    df = pd.DataFrame(cashies, columns=['month', 'year', 'earned']).\
        groupby(['year', 'month']).agg({'earned': 'sum'})

    df['date'] = [datetime.date(x[0], x[1], 1) for x in df.index]
    df['cumsum'] = df['earned'].cumsum()

    the_script, the_div = create_barplot(df)
    context = {}
    context['barplot_script'] = the_script
    context['barplot_div'] = the_div

    ytd_script, ytd_div = create_ytdplot(df)
    context['ytdplot_script'] = ytd_script
    context['ytdplot_div'] = ytd_div

    return render(request, 'reports/plots.html', context)
