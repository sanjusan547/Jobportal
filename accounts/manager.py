from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy 

class CustomUserManager(BaseUserManager):
    def create_user(self,email,password,**extra_fields):
        if not email:
            raise ValueError("The email is needed")
        email=self.normalize_email(email)
        user=self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self,email,password,**extra_fields):
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault("is_active",True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("superuser is_staff is true")
        
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("superuser is_super is true")
        return self.create_user(email,password,**extra_fields)