from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Jobseekerprofile,Employerprofile,Job,Application,Savedjob,Companyprofile,Companyreview,Globalotp,Employerreview
from django import forms
from django.core.exceptions import ValidationError
from accounts.models import User 


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'fullname', 'role', 'is_verified', 'is_staff')
    ordering = ('email',)
    search_fields = ('email', 'fullname')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('fullname', 'phonenumber', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'fullname', 'phonenumber', 'role', 'password1', 'password2'),
        }),
    )

class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = Companyprofile
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 👇 This limits the employer dropdown to only users with role='employer'
        self.fields['employer'].queryset = User.objects.filter(role='employer')


    def clean_employer(self):
        employer = self.cleaned_data['employer']
        if employer.role != 'employer':
            raise ValidationError("Only users with role 'employer' can be assigned as company owners.")
        return employer
    
class CompanyprofileAdmin(admin.ModelAdmin):
    form = CompanyProfileForm

admin.site.register(User, CustomUserAdmin)
admin.site.register(Jobseekerprofile)
admin.site.register(Employerprofile)
admin.site.register(Job)
admin.site.register(Application)
admin.site.register(Savedjob)
admin.site.register(Companyprofile,CompanyprofileAdmin)
admin.site.register(Companyreview)
admin.site.register(Globalotp)
admin.site.register(Employerreview)


