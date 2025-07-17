from django.urls import path,include
from .views import AccountHome,Registerapi,Logoutview,Savejobview,Unsavejobview,Savedjoblistview,reset_password
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    
)
from rest_framework.routers import DefaultRouter
from .views import (
                    Joblistview,
                    Jobseekerviewset,
                    Employerviewset,
                    Jobviewset,
                    Jobdetailview,
                    Applicationcreateview,
                    Applicationlistview,
                    Employerapplicationview,
                    Employerupdateview,
                    Applicationdetailview,
                    Companyprofileview,
                    Companyprofiledetailupdateview,
                    Companyreviewreplyview,
                    Publiccompanyreviewlist,
                    Employerowncompanyreviewlist,
                    Companyreviewcreateview,
                    Employerreviewview,
                    Employerreviewlist,
                    Companyjobslist
                    
                    
)



router=DefaultRouter()
router.register(r'jobseekerprofiles', Jobseekerviewset)
router.register(r'employerprofiles',Employerviewset)
router.register(r'jobs',Jobviewset)


urlpatterns = [
    path('register/', Registerapi.as_view(), name='register'),
    path('', AccountHome.as_view(), name='account-home'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/logout/',Logoutview.as_view(), name='logout'),
    path('api/joblist/', Joblistview.as_view(), name='job-list'),
    path('api/jobdetail/<int:pk>/', Jobdetailview.as_view(), name='job-detail'),
    path('api/apply/', Applicationcreateview.as_view(), name='applyjob'),
    path('api/myapplications/', Applicationlistview.as_view(), name='myapplications'),
    path('api/savejob/',Savejobview.as_view(), name='savejob'),
    path('api/employer/job/<int:job_id>/applications/',Employerapplicationview.as_view(), name='employer-applications'),
    path('api/employer/applications/<int:pk>/update/',Employerupdateview.as_view(), name='application-update'),
    path('api/employer/applications/<int:pk>/',Applicationdetailview.as_view(),name='application-detailview'),
    path('api/unsavedjob/<int:job_id>/', Unsavejobview.as_view(), name='unsavedjob'),
    path('api/savedjoblist/', Savedjoblistview.as_view(), name='savedjoblist'),
    path('api/company/create/',Companyprofileview.as_view(), name='create-company'),
    path('api/company/my',Companyprofiledetailupdateview.as_view(),name='update-company'),
    path('api/company/my/reviews/', Employerowncompanyreviewlist.as_view(), name='employer-own-reviews'),
    path('api/company/my/reviews/<int:pk>/reply/', Companyreviewreplyview.as_view(), name='company-review-reply'),
    path('api/company/review/create/', Companyreviewcreateview.as_view(), name='company-review-create'),
    path('api/company/<int:company_id>/reviews/', Publiccompanyreviewlist.as_view(), name='company-review-list'),
    path('api/company/<int:company_id>/jobs/',Companyjobslist.as_view(), name='company-job-list'),
    path('api/resetpassword/',reset_password,name='reset-password'),
    path('api/employerreview/',Employerreviewview.as_view(),name='employer-reviewview'),
    path('api/reviewview/<int:job_id>/',Employerreviewlist.as_view(),name='employerreviewview'),
    path('api/',include(router.urls))
]