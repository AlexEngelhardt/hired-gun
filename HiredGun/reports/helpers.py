import datetime

def get_initial_values():
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
