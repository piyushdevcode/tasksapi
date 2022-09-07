from rest_framework import serializers
from rest_framework.serializers import ValidationError
from taskapi.models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    task = serializers.HyperlinkedRelatedField(view_name='task-detail',many=True,read_only=True)
    # tasks = serializers.PrimaryKeyRelatedField(read_only=True)

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
    # team_leader = serializers.StringRelatedField()
    # team_members = serializers.StringRelatedField(many=True)
    # leader_url = serializers.HyperlinkedRelatedField(view_name='user-detail',read_only=True)

    ## Custom Serializer We can now specify the fields to serialize
    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def validate_team_leader(self,value):
        """
        To validate a Team Leader
        """
        leader_id = value.id
        print('printing lead_value: ',value)
        print('printing lead_id: ',leader_id)
        try:
            leader = User.objects.get(pk=leader_id)
            if  not leader.is_team_leader:
                raise ValidationError('Leader Must have `Role` of Team Leader ')
        except User.DoesNotExist:
            raise ValidationError('Team Leader doesn\'t exist ')
        return value

       
    # def validate_team_members(self,value):
    #     print('Validating Team Members...')
    #     print(value)
    #     team_members = value

    #     for _member in team_members:
    #         try:
    #             member = User.objects.get(pk=_member.id)
    #             print("Member is: ",member)
    #             if  member.is_team_member:
    #                 raise ValidationError('Member must have `Role` of Team Member ')
    #         except User.DoesNotExist:
    #             raise ValidationError('Member doesn\'t exist')
    #     return value

    class Meta:
        model = Team
        # fields = ['url','team_leader','leader_url','team_members']
        fields = '__all__'
    
class TaskSerializer(serializers.ModelSerializer):
    # team = serializers.HyperlinkedRelatedField(view_name='team-detail',read_only=True)
    # team = TeamSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ['id','name','team','started_at','completed_at','status','team_members']
        read_only_fields = ['team_members',]
