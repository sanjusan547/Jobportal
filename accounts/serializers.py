from rest_framework import serializers
from .models import User
from .models import Jobseekerprofile,Employerprofile,Job,Application,Savedjob,Companyprofile,Companyreview

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

class Applicationserializer(serializers.ModelSerializer):
     class Meta:
          model=Application
          fields='__all__'
          read_only_fields=['seeker','applied_at']

     def create(self, validated_data):
        user = self.context['request'].user
        validated_data['seeker'] = user
        return super().create(validated_data)
     
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
          
