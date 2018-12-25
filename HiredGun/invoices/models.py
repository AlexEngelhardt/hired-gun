import datetime
import re

from django.db import models
from django.db.models import F, Sum, Q

from projects.models import Project, Client, Session
from reports.helpers import get_total_earned


# Create your models here.


class Invoice(models.Model):
    invoice_no = models.CharField(max_length=128)

    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    from_date = models.DateField()
    to_date = models.DateField()
    invoice_date = models.DateField()
    paid_date = models.DateField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ['-invoice_date']

    @staticmethod
    def get_csv_head():
        line = ["ID", "invoice_no", "client", "from_date",
                "to_date", "invoice_date", "paid_date", "due_date",
                "net_amount", "gross_amount", "sessions"]
        return line

    def get_csv_line(self):

        sessions_list = list(self.session_set.values_list('id', flat=True))
        sessions_str = ",".join(map(str, sessions_list))

        line = [
            str(self.pk),
            str(self.invoice_no),
            str(self.client),
            str(self.from_date),
            str(self.to_date),
            str(self.invoice_date),
            str(self.paid_date),
            str(self.due_date),
            str(self.get_amount()),
            str(self.get_gross_total()),
            str(sessions_str)
            ]
        return line

    def __str__(self):
        return self.invoice_no

    @staticmethod
    def generate_invoice_number(user):
        """
        Generates a consecutive number starting at 0001 each year
        e.g. 2018-0001, then 2018-0002, etc.
        """
        yr = datetime.date.today().year

        this_users_invoice_nos = Invoice.objects.filter(client__user=user).\
            values_list('invoice_no')
        this_users_invoice_nos = map(lambda x: x[0], this_users_invoice_nos)
        regex = re.compile('^\d\d\d\d-(\d+)$')

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
        payment_terms = self.client.payment_terms
        if payment_terms == 'Net 30':
            due_date = datetime.date.today() + datetime.timedelta(days=30)
        elif payment_terms == 'Net 15':
            due_date = datetime.date.today() + datetime.timedelta(days=15)
        else:
            # default suggested due date: 30 days from now
            due_date = datetime.date.today() + datetime.timedelta(days=30)
        return due_date

    def is_overdue(self):
        if self.is_paid():
            return False
        else:
            return self.due_date < datetime.date.today()

    def is_paid(self):
        return self.paid_date is not None

    def get_amount(self):
        """
        Net total invoice amount
        """
        return get_total_earned(self.get_attached_sessions())

    def get_tax(self):
        return round(self.get_amount() * 0.19, 2)

    def get_gross_total(self):
        return self.get_amount() + self.get_tax()

    def get_implicit_projects(self):
        """
        Because you can create an invoice without specifying a project list,
        here we define a method that actually gets all projects that appear
        in this invoice.
        We also annotate them and add the fields units_worked, and amount,
        to be able to break down invoice positions per project
        """
        attached_sessions = self.get_attached_sessions()
        project_ids = attached_sessions.values_list('project').distinct()
        projects = Project.objects.filter(pk__in=project_ids)

        # TODO this looks like duplicate logic. I'm sure this can be refactored
        # nicely somehow. Maybe a custom Manager()?
        projects = projects.annotate(
            units_worked=Sum(F('session__units_worked'),
                             filter=Q(
                                 session__invoice=self.pk
                             )),
            amount=F('units_worked') * F('rate')
        )
        return projects

    def get_attached_sessions(self):
        qs = Session.objects.filter(
            invoice=self.pk
        )
        return qs
