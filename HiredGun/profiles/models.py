from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Profile(models.Model):
    """
    From here:
    https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html
    """
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # User model already has: firstname, lastname, email
    # firstname = models.CharField(max_length=128)
    # lastname = models.CharField(max_length=128)
    # email = models.CharField(max_length=128)
    
    address = models.TextField(default="TODO please enter address")
    phone = models.CharField(max_length=128, default="TODO please enter phone no")
    website = models.CharField(max_length=256, blank=True, null=True)

    bank_acct = models.CharField(max_length=128, default="TODO please enter bank account no")
    bank_sort_code = models.CharField(max_length=128, default="TODO please enter bank sort code")
    paypal = models.CharField(max_length=128, blank=True, null=True)

    IBAN = models.CharField(max_length=128, default="TODO please enter IBAN")
    BIC = models.CharField(max_length=128, default="TODO please enter BIC")
    tax_id = models.CharField(max_length=128, default="TODO enter tax ID here")
    

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

# https://coderwall.com/p/ktdb3g/django-signals-an-extremely-simplified-explanation-for-beginners
@receiver(post_save, sender=User)
def ensure_profile_exists(sender, **kwargs):
    if kwargs.get('created', False):
        Profile.objects.get_or_create(user=kwargs.get('instance'))

