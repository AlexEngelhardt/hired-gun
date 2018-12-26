from django.db import models
from django.contrib.auth.models import User


class SideProject(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,
                             null=True, blank=True)
    name = models.CharField(max_length=512)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        # The string representation of a single instance
        return self.name


class SideIncome(models.Model):
    side_project = models.ForeignKey(SideProject, on_delete=models.PROTECT)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    net_amount = models.DecimalField(max_digits=9, decimal_places=2,
                                     blank=False, null=False)
