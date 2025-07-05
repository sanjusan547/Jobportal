from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Jobseekerprofile,Employerprofile,Job,Application,Savedjob,Companyprofile,Companyreview,Globalotp

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

admin.site.register(User, CustomUserAdmin)
admin.site.register(Jobseekerprofile)
admin.site.register(Employerprofile)
admin.site.register(Job)
admin.site.register(Application)
admin.site.register(Savedjob)
admin.site.register(Companyprofile)
admin.site.register(Companyreview)
admin.site.register(Globalotp)


