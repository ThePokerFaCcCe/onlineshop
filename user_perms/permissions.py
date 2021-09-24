from rest_framework import permissions


class IsOwnerOfItem(permissions.BasePermission):
    def has_object_permission(self, req, view, obj):
        obj_user = obj

        if hasattr(obj, 'user'):
            obj_user = obj.user
        elif hasattr(obj, 'customer'):
            obj_user = obj.customer

        return obj_user == req.user

class IsAdmin(permissions.IsAdminUser): 
    def has_object_permission(self, request, view, obj):
        # The reason I created this class and I didn't used IsAdminUser:
        # In BasePermission class this function always returns True,
        # so I have to override it to works correct with IsOwnerOfItem
        return self.has_permission(request=request,view=view)

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, req, view):
        if req.method in permissions.SAFE_METHODS:
            return True
        elif req.user.is_authenticated:
            return (req.user.is_staff or req.user.is_admin)

    def has_object_permission(self, req, view, obj):
        if req.method in permissions.SAFE_METHODS:
            return True
        elif req.user.is_authenticated:
            return (req.user.is_staff or req.user.is_admin)


class IsSuperUser(permissions.BasePermission):
    def has_permission(self, req, view):
        if req.user.is_authenticated:
            return req.user.is_admin
