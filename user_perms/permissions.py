from rest_framework import permissions

class IsOwnerOfItem(permissions.BasePermission):
    def has_object_permission(self,req,view,obj):
        return obj.user == req.user
