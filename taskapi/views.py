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
    return Response({
        'users': reverse('user-list',request=request),
        'teams': reverse('team-list',request=request),
        'tasks': reverse('task-list',request=request),
    })


class TaskViewSet(viewsets.ModelViewSet):
    def get_permissions(self):
        """
        give create permission to USER Role only
        """
        if self.action == 'create':
            permission_classes = [IsUser | permissions.IsAdminUser]
        else:
            permission_classes = [IsMemberOfTask]
        return [permission() for permission in permission_classes]

    queryset = Task.objects.all()
    serializer_class = serializers.TaskSerializer

    #/ TRANSFER  send mail TO perform create
    def perform_create(self, serializer):
            ## ADD THE SEND MAIL HERE
        task_name = serializer.validated_data["name"]
        leader_email = serializer.validated_data["team"].team_leader.email
        print(f'Alloted to Team: {leader_email} | {task_name}')
        send_mail_to_leader.delay(from_mail='noreply@tasks.com',
                                  subject ='New Task Assigned',
                                  to_mail=['teamleadermail'],
                                  message=['hello new task alloted','taskname'],
                                  onsuccess='Task Creation mail sent successfully',)
        raise Exception
        return super().perform_create(serializer)

    
    # Only Team Leader can update all the fields of Task using PUT method
    def update(self,request,*args,**kwargs):
        print(f'Self is: {self} \nRequest: {request.data} length: ({ len(request.data)}) \nargs: {args} \n kwargs: {kwargs}')
        partial = kwargs.pop('partial',False)

        if partial or request.user.is_team_leader:
            instance = self.get_object()
            print(f'Instance Team ID: {instance.team.id}')
            serializer = self.get_serializer(instance,data=request.data,partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        
        return Response({'error':'Team Members can only modify the Status field using PATCH method'})
        
    # Team members can only update the status field
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        if request.user.is_team_leader or (len(request.data)==1 and "status" in request.data):
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

    def list(self, request, *args, **kwargs):
        queryset = Team.objects.all()
        serializer = serializers.TeamSerializer(queryset, many=True)
        print(f'Team List: {request} \n hooo \n {request.data}')
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    queryset = Team.objects.all()
    serializer_class = serializers.TeamSerializer
