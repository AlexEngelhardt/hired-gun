import datetime
import re

from django.db import models

from projects.models import Project, Client, Session
from reports.helpers import get_total_earned

# Create your models here.

class Invoice(models.Model):
    invoice_no = models.CharField(max_length=128)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    project = models.ManyToManyField(Project)
    from_date = models.DateField()
    to_date = models.DateField()
    invoice_date = models.DateField()
    paid_date = models.DateField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.invoice_no

    @staticmethod
    def generate_invoice_number(user):
        """
        Generates a consecutive number starting at 0001 each year
        e.g. 2018-0001, then 2018-0002, etc.
        """
        yr = datetime.date.today().year

        this_users_invoice_nos = Invoice.objects.filter(client__user=user).values_list('invoice_no')
        this_users_invoice_nos = map(lambda x: x[0], this_users_invoice_nos)
        regex = re.compile('.*-(\d+)$')
        
        good_invoice_nos = filter(regex.search, this_users_invoice_nos)
        nums = map(lambda x: regex.match(x).group(1), good_invoice_nos)
        
        nums = map(int, nums)
        try:
            no = max(nums) + 1
        except ValueError:
            # if no invoices (with the fitting format) have yet been created
            no = 1
        
        return str(yr) + '-' + str(no).zfill(4)
        
    def compute_due_date(self):
        # TODO: I must find all (multiple!) projects' invoicing terms,
        #  and check if they are equal. Iff they are, compute the due date.
        pass

    def is_overdue(self):
        return self.due_date < datetime.date.today()

    def is_paid(self):
        return self.paid_date is not None

    def get_amount(self):
        """
        Net total invoice amount
        """
        amount = get_total_earned(self.get_attached_sessions())
        return amount

    def get_attached_sessions(self):
        qs = Session.objects.filter(
            project__client=self.client
        )
        if self.project.count() != 0:  # if no projects attached, just use all available
            qs = qs.filter(
                project__in=self.project.all()
            )
        return qs
