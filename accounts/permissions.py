from rest_framework import permissions


class IsEmployerOfJob(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.job.employer == request.user
    
class IsEmployerUser(permissions.BasePermission):
    def has_permission(self, request, view):
        # Assuming `user.role` or `user.is_employer` is how you identify employers
        return request.user.is_authenticated and request.user.role == 'employer'