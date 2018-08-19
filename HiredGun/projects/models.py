import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=256)
    billing_address = models.TextField(null=True, blank=True)
    invoice_email = models.EmailField(max_length=256, null=True, blank=True)
    payment_terms = models.CharField(max_length=20,
                                     choices=(
                                         ('Net 15', '15 days after invoice date'),
                                         ('Net 30', '30 days after invoice date'),
                                         ('21 MFI', '21st of the month following the invoice date'),
                                         ('2% 10 Net 30', '2% discount if payment received within ten days, otherwise Net 30'),
                                         ('COD', 'Cash on delivery'),
                                         ('PIA', 'Payment in advance'),
                                     ),
                                     default='Net 30')

    @staticmethod
    def get_csv_head():
        # TODO can I do this automatically somehow, looping over all fields?
        line = ["ID", "user", "name", "billing_address", "invoice_email", "payment_terms"]
        return line
    
    def get_csv_line(self):
        line = [
            str(self.pk),
            str(self.user),
            str(self.name),
            str(self.billing_address),
            str(self.invoice_email),
            str(self.payment_terms)
            ]
        return line
        
    def __str__(self):
        # The string representation of a single instance
        return self.name
    

class Project(models.Model):
    name = models.CharField(max_length=512)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    rate = models.DecimalField(max_digits=7, decimal_places=2)
    rate_unit = models.CharField(max_length=3,
                                 choices=(
                                     ('hr', 'Hour'),
                                     ('day', 'Day'),
                                     ('fixed', 'Fixed'),
                                 ),
                                 default='hr')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.name


    @staticmethod
    def get_csv_head():
        line = ["ID", "name", "client", "rate", "rate_unit", "start_date", "end_date",
                "notes"]
        return line
    
    def get_csv_line(self):
        line = [
            str(self.pk),
            str(self.name),
            str(self.client),
            str(self.rate),
            str(self.rate_unit),
            str(self.start_date),
            str(self.end_date),
            str(self.notes)
            ]
        return line
    
    def is_active(self):
        today = datetime.date.today()
        if self.end_date is None:
            return self.start_date <= today
        else:
            return self.start_date <= today <= self.end_date
        
    # The following three *method properties* customize how the Admin panel for Project lists shows this field:
    # (see https://docs.djangoproject.com/en/2.0/intro/tutorial07/ )
    is_active.admin_order_field = 'end_date'
    is_active.boolean = True
    is_active.short_description = 'PROJ Active?'
        
    def ended_recently(self):
        if self.end_date is None:
            return False
        else:
            # check that the end date is far enough in the past AND
            #  not in the future
            return datetime.date.today() - datetime.timedelta(days=31) <= \
                self.end_date <= \
                datetime.date.today()


class Session(models.Model):
    project = models.ForeignKey(Project, on_delete=models.PROTECT)
    date = models.DateField()

    # You can't `from invoices.models import Invoice` here, because that would be a circular import.
    # Instead, you can just write the referenced model as a string here:
    invoice = models.ForeignKey('invoices.Invoice', on_delete=models.SET_NULL, blank=True, null=True)
    
    # I want to supply either "units worked" (e.g. 0.5 days), or a start and end time, and have
    #  the app compute the number of hours / days itself
    units_worked = models.DecimalField(max_digits=4, decimal_places=2)

    # Only units_worked is required. But if you supply these 3 fields, it can be auto-computed later
    #  (you might have to use that Ajax thingy, or jQuery, or whatever)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    break_duration = models.DurationField(blank=True, null=True) # default=datetime.timedelta(minutes=30))

    description = models.TextField(blank=True, null=True)
    # If I'll use a 'duration' field, it should be blank=True but null=False, so that it has to be auto-generated

    @staticmethod
    def get_csv_head():
        # TODO can I do this automatically somehow, looping over all fields?
        line = ["ID", "project", "date", "invoice", "units_worked",
                "start_time", "end_time", "break_duration", "description"]
        return line
    
    def get_csv_line(self):
        line = [
            str(self.pk),
            str(self.project),
            str(self.date),
            str(self.invoice),
            str(self.units_worked),
            str(self.start_time),
            str(self.end_time),
            str(self.break_duration),
            str(self.description)
            ]
        return line

    
    def get_units_worked(self):
        # TODO maybe I can auto-compute this value later, instead of specifying it every time
        return self.units_worked
    
    def get_money_earned(self):
        # TODO this is redunantly computed in views.py too :(
        return self.units_worked * self.project.rate

    def __str__(self):
        return 'Session in ' + str(self.project) + \
           ' for ' + str(self.project.client)  + \
           ' on ' + str(self.date)
