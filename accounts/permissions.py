from rest_framework import permissions


class IsEmployerOfJob(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.job.employer == request.user