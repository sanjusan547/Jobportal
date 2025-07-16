from django.db import models
import enum
from  django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from .manager import CustomUserManager
from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
class RoleEnum(enum.Enum):
    JOBSEEKER = 'jobseeker'
    EMPLOYER = 'employer'


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ( RoleEnum.JOBSEEKER.value,'jobseeker'),
        ( RoleEnum.EMPLOYER.value,'employer'),
    )
    
    email=models.EmailField(unique=True)
    fullname=models.CharField(max_length=100)
    phonenumber=models.CharField(max_length=100,null=True)
    role=models.CharField(max_length=10,choices=ROLE_CHOICES,default="")
    is_verified=models.BooleanField(default=False)


    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['fullname','phonenumber','role']
    
    objects=CustomUserManager()
    def __str__(self):
        return self.email

class Jobseekerprofile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    resume=models.FileField(upload_to='resumes/',blank=True,null=True)
    skills=models.TextField(blank=True)
    education=models.TextField
    experience=models.CharField(max_length=225,blank=True,null=True)

    def __str__(self):
        return f"jobseeker:{self.user.email}"
    
class Employerprofile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    companyname=models.CharField(max_length=225)
    website=models.URLField(blank=True,null=True)

    def __str__(self):
        return f"Employer:{self.user.email}"
    
class Job(models.Model):
    JOB_TYPE_CHOICES=[
                ("parttime","PARTTIME"),
                ("fulltime","FULLTIME"),
                ("internship","INTERNSHIP"),
                ("remote","REMOTE"),
    ]

    employer=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    title=models.CharField(max_length=255)
    description=models.TextField()
    jobtype=models.CharField(max_length=20,choices=JOB_TYPE_CHOICES)
    location=models.CharField(max_length=255)
    salary=models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)
    experience=models.IntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    interview_date=models.DateField(blank=True,null=True)
    interview_time=models.TimeField(blank=True,null=True)
    interview_venue=models.TextField(blank=True,null=True)
    walkin_drive=models.BooleanField(default=False,blank=True,null=True)

    def __str__(self):
        return self.title


class Application(models.Model):
    job=models.ForeignKey(Job,on_delete=models.CASCADE,related_name="applications")
    seeker=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    coverletter=models.TextField(blank=True,null=True)
    resume=models.FileField(upload_to='resumes/',blank=True,null=True)
    applied_at=models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),('seen','Seen')
    ]
    status=models.CharField(max_length=20, choices=STATUS_CHOICES,default='pending')
    
    class Meta:
        unique_together=('seeker','job')

    def __str__(self):
        return f'{self.seeker} applied for {self.job}'
    

class Savedjob(models.Model):
    seeker=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    job=models.ForeignKey('Job',on_delete=models.CASCADE) # 'Job' string representation avoid circular imports
    saved_at=models.DateTimeField(auto_now=True)

    class Meta:
        unique_together=('seeker','job')

    def __str__(self):
        return f'{self.seeker} saved {self.job}'
    
class Companyprofile(models.Model):
    employer=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    name=models.CharField(max_length=255)
    description=models.TextField()
    website=models.URLField(blank=True,null=True)
    logo=models.ImageField(upload_to='company-logo',blank=True,null=True)

    def __str__(self):
        return self.name
    
class Companyreview(models.Model):
    company=models.ForeignKey('Companyprofile',on_delete=models.CASCADE,related_name='reviews')
    reviewer=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    rating=models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    comment=models.TextField(blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    reply=models.TextField(blank=True,null=True)
    reply_at=models.DateTimeField(blank=True,null=True)

    class Meta:
        unique_together=('reviewer','company')

    def __str__(self):
        return f"{self.company} - {self.reviewer} - {self.rating}"
    
class Globalotp(models.Model):
    otp=models.CharField(max_length=100)
    created_at=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"otp:{self.otp} at {self.created_at}"
class Employerreview(models.Model):
    job=models.ForeignKey(Job,on_delete=models.CASCADE,related_name='review')
    employer=models.ForeignKey(User,on_delete=models.CASCADE)
    review=models.TextField()
    rating=models.PositiveBigIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self,):
        return f"Review added for job {self.job} by {self.employer}"