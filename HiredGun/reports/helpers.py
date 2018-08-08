import datetime
from projects.models import Session

def get_initial_values():
    """
    Gets default values to put into the report forms.
    We check for the most recent ("youngest") session entered, 
    and the default values create a report for that entire month.
    """
    
    youngest_session = Session.objects.order_by('date').last()
    youngest_date_with_sessions = youngest_session.date

    first_of_that_month = youngest_date_with_sessions.replace(day=1)
    last_of_that_month = (first_of_that_month.replace(day=28) + datetime.timedelta(days=4)).replace(day=1) - datetime.timedelta(days=1)
    
    # TODO rename the variables to sth now meaningful. It's not "previous_month" anymore
    context = {
        'previous_month': first_of_that_month.month,
        'year_of_previous_month': first_of_that_month.year,
        'first_of_prev_month': first_of_that_month.strftime('%Y-%m-%d'),
        'last_of_prev_month': last_of_that_month.strftime('%Y-%m-%d')
    }
    return context
        
