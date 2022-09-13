from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.viewsets import generics
from rest_framework.viewsets import mixins
from rest_framework.decorators import permission_classes, api_view

from taskapi.models import *
from taskapi import serializers
from taskapi.permissions import *
from rest_framework.reverse import reverse
from rest_framework import permissions, status
from rest_framework.response import Response
from django.core.mail import send_mail
from core.tasks import send_mail_to_leader

@api_view()
def root_API(request):
    """
    Root API for Task-api
    """
    return Response({
        'users': reverse('user-list',request=request),
        'teams': reverse('team-list',request=request),
        'tasks': reverse('task-list',request=request),
    })


class TaskViewSet(viewsets.ModelViewSet):
    def get_permissions(self):
        """
        give create permission to USER Role only else only Members of Task can access
        """
        if self.action == 'create':
            permission_classes = [IsUser | permissions.IsAdminUser]
        else:
            permission_classes = [IsMemberOfTask]
        return [permission() for permission in permission_classes]

    queryset = Task.objects.all()
    serializer_class = serializers.TaskSerializer
     
    def perform_create(self, serializer):
        """
        when new task is created send mail to their corresponding leader
        """
        task_name = serializer.validated_data["name"]
        leader    = serializer.validated_data["team"].team_leader
        message   = f'Hello {leader.username},\n\nNew Task "{task_name}" is assigned to your team'
        subject   = f'New Task {task_name} Assigned'
        send_mail_to_leader.delay(subject =subject,
                                  to_email=leader.email,
                                  message=message,
                                  onsuccess='Task Creation mail sent successfully')
        # raise Exception
        serializer.save()
    
    # Only Team Leader can update all the fields of Task using PUT method
    def update(self,request,*args,**kwargs):
        print(f'Self is: {self} \nRequest: {request.data} length: ({ len(request.data)}) \nargs: {args} \n kwargs: {kwargs}')
        partial = kwargs.pop('partial',False)

        # if PATCH Request or user is team leader
        if partial or request.user.is_team_leader:
            instance = self.get_object()
            print(f'Instance Team ID: {instance.team.id}')
            serializer = self.get_serializer(instance,data=request.data,partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        
        return Response({'error':'Team Members can only modify the Status field using PATCH method'})
        
    # Team members can only update the status field using PATCH
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        only_editing_status = bool((len(request.data)==1 and "status" in request.data))
        if request.user.is_team_leader or only_editing_status:
            return super().partial_update(request, *args, **kwargs)
    
        return Response({'error':'Team Members can only modify the status field'})
        

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAdminUser]

class TeamViewSet(viewsets.ModelViewSet):
    def get_permissions(self):
        """
        give create permission to USER and ADMIN Role only
        """
        if self.action == 'create':
            permission_classes = [IsUser | permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]


    queryset = Team.objects.all()
    serializer_class = serializers.TeamSerializer
