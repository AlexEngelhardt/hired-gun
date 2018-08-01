import datetime

from django.db import models
from django.utils import timezone


class Client(models.Model):
    name = models.CharField(max_length=256)
    billing_address = models.CharField(max_length=512)
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
                                 ),
                                 default='hr')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

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
    start_time = models.TimeField()
    end_time = models.TimeField()
    break_duration = models.DurationField(default=datetime.timedelta(minutes=30))
    description = models.TextField()
    # If I'll use a 'duration' field, it should be blank=True but null=False, so that it has to be auto-generated
    
    def __str__(self):
        return 'Session in ' + str(self.project) + \
           ' for ' + str(self.project.client)  + \
           ' on ' + str(self.date)
