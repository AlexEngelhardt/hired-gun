import datetime

from django.db import models

from projects.models import Project, Client

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

    def generate_invoice_number(self):
        # TODO
        pass
        
    def compute_due_date(self):
        # TODO: I must find all (multiple!) projects' invoicing terms,
        #  and check if they are equal. Iff they are, compute the due date.
        pass

    def is_overdue(self):
        return self.due_date < datetime.date.today()

    def is_paid(self):
        return self.paid_date is not None

    def get_amount(self):
        # TODO
        return 666
