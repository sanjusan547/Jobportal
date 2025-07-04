from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Employerprofile,Jobseekerprofile,User


@receiver(post_save,sender=User)
def createuserprofile(sender,created,instance,**kwargs):
    if created:
        if instance.role == 'employer':
            Employerprofile.objects.create(user=instance)
        elif instance.role=='jobseeker':
            Jobseekerprofile.objects.create(user=instance)
        
    
