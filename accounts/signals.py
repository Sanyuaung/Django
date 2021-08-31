from django.db.models.signals import post_save
from django.contrib.auth.models import User,Group
from accounts.models import Customer

def create_customer_profile(sender,instance,created,**kwargs):
    if created :
        gp=Group.objects.get(name="Customer")
        instance.groups.add(gp)
        Customer.objects.create(user=instance,email=instance.email)

post_save.connect(create_customer_profile,sender=User)