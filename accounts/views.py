from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import Register
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken,TokenError
from rest_framework import status
from .models import Jobseekerprofile,Employerprofile,Job,Application,Savedjob,Companyprofile,Companyreview,Globalotp,User,Employerreview
from .serializers import(
     Jobseekerserializer,
     Employerserializer,
     Jobserializer,
     Applicationserializer,
     Savedjobserializer,
     Companyprofileserializer,
     Companyreviewserializer,
     Companyreviewreplyserializer,
     Employerreviewserializer
)
from rest_framework import viewsets,permissions,generics,filters
from.filters import Jobfilter
import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsEmployerOfJob
from rest_framework.exceptions import PermissionDenied,ValidationError
from django.utils import timezone
from rest_framework.decorators import api_view,permission_classes
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from datetime import timedelta
from .utils import send_notification_mail
from drf_yasg.utils import swagger_auto_schema





class Registerapi(APIView):
    def post(self,request):
        serializer = Register(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AccountHome(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"message": "Welcome to the Account API Home"})
    
class Logoutview(APIView):
    permission_classes=[IsAuthenticated]

    def post(self,request):
        try:
            refresh_token=request.data["refresh"]
            token=RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logout successful"},status=status.HTTP_200_OK)
        except KeyError:
            return Response({"detail": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
        except TokenError:
            return Response({"detail": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)
        
class Jobseekerviewset(viewsets.ModelViewSet):
    queryset=Jobseekerprofile.objects.all()
    serializer_class=Jobseekerserializer
    permission_classes=[IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class Employerviewset(viewsets.ModelViewSet):
    queryset=Employerprofile.objects.all()
    serializer_class=Employerserializer
    permission_classes=[IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class IsEmployer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'employer'
class Jobviewset(viewsets.ModelViewSet):
    queryset=Job.objects.all()
    serializer_class=Jobserializer
    permission_classes=[permissions.IsAuthenticated,IsEmployer]

    def perform_create(self, serializer):
        user=self.request.user
        if user.role != 'employer':
            raise PermissionDenied("only employers can post jobs")
        try:
            company=Companyprofile.objects.get(employer=user)
        except Companyprofile.DoesNotExist:
            raise ValidationError("first you need to create a company profile")
        serializer.save(employer=user,company=company)

class Joblistview(generics.ListAPIView):
    queryset=Job.objects.all()
    serializer_class=Jobserializer
    permission_classes=[permissions.AllowAny]
    filter_backends=[DjangoFilterBackend,filters.SearchFilter]
    filterset_class=Jobfilter
    search_fields=['title','description',]
@swagger_auto_schema(responses={200: Jobserializer(many=True)})

class Jobdetailview(generics.RetrieveAPIView):
    queryset=Job.objects.all()
    serializer_class=Jobserializer
    permission_classes=[permissions.AllowAny]

class Applicationcreateview(generics.CreateAPIView):
    queryset=Application.objects.all()
    serializer_class=Applicationserializer
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serializer):
        application = serializer.save(seeker=self.request.user)

        # Send email after saving
        subject = 'Application Received'
        message = f"Dear {self.request.user.fullname},\n\nYour application for the job '{application.job.title}' has been received.\n\nThank you!"
        send_notification_mail(subject, message, self.request.user.email)

class Applicationlistview(generics.ListAPIView):
    serializer_class=Applicationserializer             #serializer class tells views which serializer will use
    permission_classes=[permissions.IsAuthenticated]
    def get_queryset(self):
        return Application.objects.filter(seeker=self.request.user)      # when authenciated user can see their owm applications

class Savejobview(generics.CreateAPIView):
    serializer_class=Savedjobserializer
    permission_classes=[permissions.IsAuthenticated]   

class Unsavejobview(generics.DestroyAPIView):
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        user=self.request.user
        return Savedjob.objects.filter(seeker=user)
    def get_object(self):
        job_id=self.kwargs['job_id']
        return self.get_queryset().get(job_id=job_id)
    
class Savedjoblistview(generics.ListAPIView):
    serializer_class=Savedjobserializer
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        return Savedjob.objects.filter(seeker=self.request.user)
    
class Employerapplicationview(generics.ListAPIView):
    serializer_class=Applicationserializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        jobid=self.kwargs['job_id']
        return Application.objects.filter(
            job_id=jobid,
            job__employer=self.request.user

        )

class Employerupdateview(generics.UpdateAPIView):
    queryset=Application.objects.all()
    serializer_class=Applicationserializer
    permission_classes=[IsAuthenticated,IsEmployerOfJob]

class Applicationdetailview(generics.RetrieveAPIView):
    queryset=Application.objects.all()
    serializer_class=Applicationserializer
    permission_classes=[IsAuthenticated,IsEmployerOfJob]

    def retrieve(self, request, *args, **kwargs):
        instance=self.get_object()
        if instance.status=='pending':
            instance.status = 'seen'
            instance.save()
        return super().retrieve(request, *args, **kwargs)
    
class Companyprofileview(generics.CreateAPIView):
    serializer_class=Companyprofileserializer
    permission_classes=[IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.role !='employer':
            raise PermissionDenied("Only Employers can create company profile")
        if Companyprofile.objects.filter(employer=self.request.user).exists():
            raise PermissionDenied("you have already created a companyprofile")
        serializer.save(employer=self.request.user)

class Companyprofiledetailupdateview(generics.RetrieveUpdateAPIView):
    serializer_class=Companyprofileserializer
    permission_classes=[IsAuthenticated]

    def get_object(self):
        user=self.request.user
        if user.role != 'employer':
            raise PermissionDenied("only employers can access this")
        try:
            return Companyprofile.objects.get(employer=user)
        except Companyprofile.DoesNotExist:
            raise PermissionDenied("company profile does not exist")
        
class Companyreviewcreateview(generics.CreateAPIView):
    serializer_class = Companyreviewserializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        if user.role != 'jobseeker':
            raise PermissionDenied("Only jobseekers can post reviews.")
        serializer.save(reviewer=user)
        
class Publiccompanyreviewlist(generics.ListAPIView):
    serializer_class=Companyreviewserializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        company_id=self.kwargs['company_id']
        return Companyreview.objects.filter(company_id=company_id)

class Companyjobslist(generics.ListAPIView):
    serializer_class=Jobserializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        companyid=self.kwargs['company_id']
        return Job.objects.filter(company_id=companyid)
    
class Employerowncompanyreviewlist(generics.ListAPIView):
    serializer_class=Companyreviewserializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        user=self.request.user
        if user.role != 'employer':
            raise PermissionDenied("only employers can access this")
        try:
            company=Companyprofile.objects.get(employer=user)
        except Companyprofile.DoesNotExist:
            raise PermissionDenied("You don't have company profile")
        return Companyreview.objects.filter(company=company)
    
class Companyreviewreplyview(generics.UpdateAPIView):
    serializer_class=Companyreviewreplyserializer
    permission_classes=[IsAuthenticated]
    queryset=Companyreview.objects.all()

    def perform_update(self, serializer):
        review=self.get_object()
        user=self.request.user

        if user.role != 'employer':
            raise PermissionDenied("only employers can reply to reviews")
        if review.company.employer != user:
            raise PermissionDenied("You can only reply to reviews on your own company")
        serializer.save(reply_at=timezone.now())

user= get_user_model
@api_view(['POST'])
@permission_classes([])

def reset_password(request):
    email=request.data.get('email')
    otp=request.data.get('otp')
    new_password=request.data.get('new_password')

    if not all([email,otp,new_password]):
        return Response({'error':'All fields are mandatory'},status=status.HTTP_400_BAD_REQUEST)
    try:
        global_otp=Globalotp.objects.latest('created_at')
        if otp != global_otp.otp:
            return Response({'error':"invalid otp"},status=status.HTTP_400_BAD_REQUEST)
        if timezone.now() - global_otp.created_at > timedelta(days=2):
            return Response({"error":"otp expired"},status=status.HTTP_400_BAD_REQUEST)
    
        user=User.objects.get(email=email)
        user.password=make_password(new_password)
        user.save()

        return Response({"message":"password reset successfully"},status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error":"No user found"},status=status.HTTP_404_NOT_FOUND)
    except Globalotp.DoesNotExist:
        return Response({"error":"No otp configured"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Employerreviewview(generics.CreateAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=Employerreviewserializer

    def perform_create(self, serializer):
        user=self.request.user
        job=serializer.validated_data['job']
        if job.employer != user:
            raise PermissionDenied("only employers can add review on thier own job")     
        serializer.save(employer=user)   

class Employerreviewlist(generics.ListAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=Employerreviewserializer

    def get_queryset(self):
        jobid=self.kwargs['job_id']
        return Employerreview.objects.filter(job_id=jobid)

# Create your views here.
