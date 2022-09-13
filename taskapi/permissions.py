from email import message
from rest_framework import permissions

class IsMemberOfTask(permissions.BasePermission):
    """
    Object-level permission to only allow Task members to edit it.
    """
    message = "You can't perform this action, you're not a member of this Task"

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if(obj.team.team_leader == request.user):
            return True
        team_members = obj.team_members.all()
        for member in team_members:
            if(member == request.user): 
                return True

class IsUser(permissions.BasePermission):
    """
    permission to allow only USER to create team and task
    """
    message = "You can't perform this action, only USER Role is allowed to access"
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.is_user
