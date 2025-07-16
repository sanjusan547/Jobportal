from rest_framework import serializers
from .models import User
from .models import Jobseekerprofile,Employerprofile,Job,Application,Savedjob,Companyprofile,Companyreview,Employerreview
from.utils import send_notification_mail

class Register(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model=User
        fields=['email','password','role']

    def create(self, validated_data):
          user =User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role']
          )
          return user
    
class Jobseekerserializer(serializers.ModelSerializer):
     class Meta:
          model=Jobseekerprofile
          fields='__all__'
          read_only_fields=['user']
class Employerserializer(serializers.ModelSerializer):
     class Meta:
          model=Employerprofile
          fields='__all__'
          read_only_fields=['user']
class Jobserializer(serializers.ModelSerializer):
     class Meta:
          model=Job
          fields='__all__'
          read_only_fields=['employer','created_at']

     def to_representation(self, instance):
        rep = super().to_representation(instance)

        # If either date or venue is missing, remove all interview-related fields
        if not instance.interview_date or not instance.interview_venue:
            rep.pop('interview_date', None)
            rep.pop('interview_time', None)
            rep.pop('interview_venue', None)
            rep.pop('walkin_drive', None)

        return rep


class Applicationserializer(serializers.ModelSerializer):
     class Meta:
          model=Application
          fields='__all__'
          read_only_fields=['seeker','applied_at']

     def create(self, validated_data):
        user = self.context['request'].user
        validated_data['seeker'] = user
        return super().create(validated_data)

     def update(self, instance, validated_data):
          
          oldstatus=instance.status
          new_status=validated_data.get('status',oldstatus)
          instance = super().update(instance, validated_data)

        # If status changed, send email
          if oldstatus != new_status:
              self.send_status_email(instance)

          return instance
     def send_status_email(self, application):
        status = application.status
        job_title = application.job.title
        first_name = application.seeker.fullname
        to_email = application.seeker.email

        if status == 'rejected':
          subject = f"Application Rejected - {job_title}"
          message = f"Dear {first_name},\n\nWe regret to inform you that your application for '{job_title}' was not selected."
        elif status == 'shortlisted':
          subject = f"You've Been Shortlisted - {job_title}"
          message = f"Dear {first_name},\n\nGood news! You’ve been shortlisted for the job '{job_title}'. We'll contact you with next steps."
        else:
          return  # No email for other statuses
        send_notification_mail(subject, message, to_email)

     def validate(self, data):
          user=self.context['request'].user
          job=data.get('job')

          if Application.objects.filter(seeker=user, job=job).exists():
            raise serializers.ValidationError("You have already applied for this job.")

          return data
     
class Savedjobserializer(serializers.ModelSerializer):
     class Meta:
          model=Savedjob
          fields='__all__'
          read_only_fields=['seeker','saved_at']

     def create(self, validated_data):
        user = self.context['request'].user
        validated_data['seeker'] = user
        return super().create(validated_data)
     
class Companyprofileserializer(serializers.ModelSerializer):
     class Meta:
          model=Companyprofile
          fields=['name','id','logo','website','description']
          read_only_fields=['id']

class Companyreviewserializer(serializers.ModelSerializer):
     reviewer_name=serializers.CharField(source='reviewer.username',read_only=True)

     class Meta:
          model=Companyreview
          fields = ['id', 'company', 'reviewer', 'reviewer_name', 'rating', 'comment', 'created_at','reply','reply_at']
          read_only_fields=['id','reviewer','created_at','reply','reply_at']

class Companyreviewreplyserializer(serializers.ModelSerializer):
     class Meta:
          model=Companyreview
          fields=['reply']
class Employerreviewserializer(serializers.ModelSerializer):
    class Meta:
        model=Employerreview
        fields='__all__'
        read_only_fields=['id','employer','created_at']

          
