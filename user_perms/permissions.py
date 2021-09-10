from rest_framework import permissions

class IsOwnerOfItem(permissions.BasePermission):
    def has_object_permission(self,req,view,obj):
        return obj.user == req.user

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, req, view):
        if req.method in permissions.SAFE_METHODS:
            return True
        elif req.user.is_authenticated:
            return (req.user.is_staff or req.user.is_admin)
    def has_object_permission(self, req, view,obj):
        if req.method in permissions.SAFE_METHODS:
            return True
        elif req.user.is_authenticated:
            return (req.user.is_staff or req.user.is_admin)

class IsSuperUser(permissions.BasePermission):
    def has_permission(self, req, view):
        if req.user.is_authenticated:
            return req.user.is_admin
        