from rest_framework import serializers
from rest_framework.serializers import ValidationError
from taskapi.models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    task = serializers.HyperlinkedRelatedField(view_name='task-detail',many=True,read_only=True)

    # to enable hidden input in password form of browsable API and hide it in Response
    password = serializers.CharField(style={'input_type': 'password'},write_only=True)

    def create(self, validated_data):
        """
            for setting password hash
        """
        user = User.objects.create(username = validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user
        
    class Meta:
        model = User
        fields = ['url','id','username','email','role','task','password']


class TeamSerializer(serializers.ModelSerializer):

    def validate_team_leader(self,value):
        """
        To validate a Team Leader
        """
        leader_id = value.id
        try:
            leader = User.objects.get(pk=leader_id)
            if  not leader.is_team_leader:
                raise ValidationError('Leader Must have `Role` of Team Leader ')
        except User.DoesNotExist:
            raise ValidationError('Team Leader doesn\'t exist ')
        return value

    def validate_team_members(self,value):
        """
        To validate a Team Member
        """
        team_members = value

        for _member in team_members:
            try:
                member = User.objects.get(pk=_member.id)
                if not member.is_team_member:
                    raise ValidationError('Member must have `Role` of Team Member ')
            except User.DoesNotExist:
                raise ValidationError('Member doesn\'t exist')
        return value

    class Meta:
        model = Team
        fields = '__all__'
    
class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ['id','name','team','started_at','completed_at','status','team_members']
        read_only_fields = ['team_members',]
