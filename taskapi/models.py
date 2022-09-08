from distutils.log import error
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    
    USER = 'User'
    TEAM_LEADER = 'Team Leader'
    TEAM_MEMBER = 'Team Member'

    ROLE_CHOICES = (
        (USER ,'User'),
        (TEAM_LEADER ,'Team Leader'),
        (TEAM_MEMBER ,'Team Member')
    )

    role = models.CharField(choices=ROLE_CHOICES,default=TEAM_MEMBER,max_length=20)
    email = models.EmailField(blank=False)

    @property
    def is_user(self):
        return self.role == User.USER
    
    @property
    def is_team_leader(self):
        return self.role == User.TEAM_LEADER

    @property
    def is_team_member(self):
        return self.role == User.TEAM_MEMBER


class Team(models.Model):
    name = models.CharField(max_length=100,blank=False)

    # using limit choice to show only the team leaders in the select input
    team_leader = models.ForeignKey(User,related_name='team_l',on_delete=models.CASCADE,limit_choices_to={'role':User.TEAM_LEADER})
    team_members = models.ManyToManyField(User,related_name='team_m',
    limit_choices_to={'role':User.TEAM_MEMBER},blank=True)

    def __str__(self) -> str:
        return f'Team {self.name} lead by {self.team_leader.username}'

class Task(models.Model):
    ASSIGNED = 'Assigned'
    IN_PROGRESS = 'In Progress'
    UNDER_REVIEW = 'Under Review'
    DONE = 'DONE'

    STATUS_CHOICES = (
        (ASSIGNED,'Assigned'),
        (IN_PROGRESS,'In Progress'),
        (UNDER_REVIEW ,'Under Review'),
        (DONE,'DONE')
    )
    team = models.ForeignKey(Team,related_name='task_t',on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=100,blank=False)
    status = models.CharField(choices=STATUS_CHOICES,default=ASSIGNED,max_length=20)
    #Will auto populate team members when saving a new Instance so setting blank
    team_members = models.ManyToManyField(User,related_name='task',blank=True)
    started_at = models.DateField(auto_now_add=True)
    completed_at = models.DateField(blank=True,null=True)

    def save(self,*args,**kwargs):
        instance = super().save(*args,**kwargs)
        print('Printing Instance of Task---')
        print("instance: ",instance,"\nself: ",self)
        team = Team.objects.get(pk=self.team.id)
        print("Team: ",team)
        members = team.team_members.all()
        for member in members:
            print("Member: ",member,"\n")
            self.team_members.add(member) 
        # raise Exception #For debugging purpose
        return self
    
    
    def __str__(self) -> str:
        return f'Task {self.id}: {self.name} alloted to {self.team.name} | {self.team.team_leader}'
