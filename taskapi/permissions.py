from email import message
from rest_framework import permissions

class IsMemberOfTask(permissions.BasePermission):
    """
    Object-level permission to only allow Task members to edit it.
    """
    message = 'You can\'t perform this action, you\'re not a member of this Task'

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if(obj.team.team_leader == request.user):
            return True
        for member in obj.team_members.all():
            if(member == request.user): 
                return True

        print('yo',"\n",obj.team_members,"\n",obj.team.team_leader)

class IsUser(permissions.BasePermission):
    """
    permission to allow only USER to create team and task
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.is_user
