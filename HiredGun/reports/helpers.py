import datetime
from projects.models import Session
from django.db.utils import OperationalError

from django.db.models import F, Sum


def get_total_earned(sessions):
    return sessions.aggregate(cash = Sum(F('units_worked') * F('project__rate')))['cash']


def get_initial_values(user):
    """
    Gets default values to put into the report forms.
    We check for the most recent ("youngest") session entered, 
    and the default values create a report for that entire month.
    """

    try: 
        youngest_session = Session.objects.filter(project__client__user=user).order_by('date').last()
        if youngest_session is not None:
            youngest_date_with_sessions = youngest_session.date
        else:
            # Just use the last calendar month if you have no sessions at all.
            youngest_date_with_sessions = datetime.date.today().replace(day=1) - datetime.timedelta(days=1)

        first_of_that_month = youngest_date_with_sessions.replace(day=1)
        last_of_that_month = (first_of_that_month.replace(day=28) + datetime.timedelta(days=4)).replace(day=1) - datetime.timedelta(days=1)
    
        # TODO rename the variables to sth now meaningful. It's not "previous_month" anymore
        context = {
            'previous_month': first_of_that_month.month,
            'year_of_previous_month': first_of_that_month.year,
            'first_of_prev_month': first_of_that_month.strftime('%Y-%m-%d'),
            'last_of_prev_month': last_of_that_month.strftime('%Y-%m-%d')
        }
    except OperationalError:
        # If you just pulled this repository and your DB is fresh,
        # trying to access the DB in a view throws an error.
        # Catch it and fall back to displaying "last month" here.
        # See:
        # https://stackoverflow.com/questions/34548768/django-no-such-table-exception/36453000
        
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
        
    return context
        
