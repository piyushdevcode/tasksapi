from rest_framework.test import APITestCase, force_authenticate
from rest_framework import status
from django.urls import reverse
from taskapi.models import *
from .test_setup import TestSetUp

class TestUserCreateRetreive(TestSetUp):
    # only superuser can create Users
    # only Team Leader can update the all task fields
    # Team Member can update the status using PATCH
    # only USER can retreive all the tasks
    def setUp(self):
        self.new_user_data = {
            'username': 'User1',
            'password': 'imuser1@gmail.com',
            'email': 'imuser1@gmail.com',
            'role': 'User'
        }
        return super().setUp()

    # non-admin trying to create a new user
    def test_user_register_non_admin(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(reverse('user-list'),self.new_user_data)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
    
    def test_user_register_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(reverse('user-list'),self.new_user_data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
    
    # non admin retrieving the info
    def test_user_retrieve_non_admin(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(reverse('user-detail',kwargs={'pk':'1'}))
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

    # admin retrieving user info 
    def test_user_retrieve_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(reverse('user-detail',kwargs={'pk':'1'}))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    # only USER Role can create Team and Tasks
class TestTeamCreate(TestSetUp):
    def setUp(self):
        super().setUp()
        self.new_team_data = {
            'name': 'Test',
            'team_leader': self.leader1.id,
            'team_members': [self.member1.id],
        }

    def test_create_team_by_non_user(self):
        self.client.force_authenticate(user=self.leader2)
        response = self.client.post(reverse('team-list'),self.new_team_data)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
        
    def test_create_team_by_USER(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(reverse('team-list'),self.new_team_data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    # assigning a user not having 'leader' role as Team Leader
    def test_create_team_by_USER_not_leader(self):
        self.new_team_data['team_leader'] = self.member1.id
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(reverse('team-list'),self.new_team_data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
    
     # assigning a user not having 'member' role as Team member
    def test_create_team_by_USER_not_leader(self):
        self.new_team_data['team_members'] = [self.user2.id]
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(reverse('team-list'),self.new_team_data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

class TaskTestCase(TestSetUp):
    def setUp(self):
        super().setUp()
        self.new_task_data = {
            'name': 'Dummy Job',
            'team' : self.team1.id,
        }

    def test_create_task_by_non_USER(self):
        self.client.force_authenticate(user=self.leader2)
        response  = self.client.post(reverse('task-list'),self.new_task_data)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

    def test_create_task_by_USER(self):
        self.client.force_authenticate(user=self.user1)
        response  = self.client.post(reverse('task-list'),self.new_task_data)
        # import pdb
        # pdb.set_trace()
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
    
    # only member or leader of given task can view task details
    def test_retreive_task_by_taskmember(self):
        self.client.force_authenticate(user=self.member2)
        response  = self.client.get(reverse('task-detail',kwargs={'pk':'1'}))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_retreive_task_by_non_taskmember(self):
        self.client.force_authenticate(user=self.leader2)
        response  = self.client.get(reverse('task-detail',kwargs={'pk':'1'}))
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

    
    
    

