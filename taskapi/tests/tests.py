from rest_framework.test import force_authenticate
from rest_framework import status
from django.urls import reverse
from taskapi.models import *
from .test_setup import TestSetUp

class TestUserCreateRetreive(TestSetUp):
    def setUp(self):
        self.new_user_data = {
            'username': 'newuser',
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
        
    # admin creating a new user
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

class TestTeamCreate(TestSetUp):
    def setUp(self):
        super().setUp()
        self.new_team_data = {
            'name': 'Test',
            'team_leader': self.leader1.id,
            'team_members': [self.member1.id],
        }

    # only USER Role can create Team
    def test_create_team_by_non_USER(self):
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
    def test_create_team_by_USER_not_member(self):
        self.client.force_authenticate(user=self.user1)
        self.new_team_data['team_members'] = [self.user2.id]
        response = self.client.post(reverse('team-list'),self.new_team_data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

class TaskTestCase(TestSetUp):
    def setUp(self):
        super().setUp()
        self.new_task_data = {
            'name': 'Dummy Job',
            'team' : self.team1.id,
        }

    # only USER Role can create Team
    def test_create_task_by_non_USER(self):
        self.client.force_authenticate(user=self.leader2)
        response  = self.client.post(reverse('task-list'),self.new_task_data)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

    def test_create_task_by_USER(self):
        self.client.force_authenticate(user=self.user1)
        response  = self.client.post(reverse('task-list'),self.new_task_data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
    
    # only USER Role can view all tasks list
    def test_retrieve_tasks_list_by_USER(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(reverse('task-list'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    # only member or leader of given task can view task details
    def test_retreive_task_by_taskmember(self):
        self.client.force_authenticate(user=self.member2)
        response  = self.client.get(reverse('task-detail',kwargs={'pk':'1'}))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_retreive_task_by_non_taskmember(self):
        self.client.force_authenticate(user=self.leader2)
        response  = self.client.get(reverse('task-detail',kwargs={'pk':'1'}))
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

    # only team leader of given can update any field of task with PUT or PATCH
    def test_update_task_by_non_leader(self):
        data = {
            'name' : 'Test Flex',
            'team' : self.team1.id,
        }
        self.client.force_authenticate(user=self.member1)
        response = self.client.put(reverse('task-detail',kwargs={'pk':'1'}),data)
        self.assertEqual(response.status_code,status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def test_update_task_by_leader(self):
        data = {
            'name' : 'Task Check',
            'team' : self.team1.id,
        }
        self.client.force_authenticate(user=self.leader1)
        response = self.client.put(reverse('task-detail',kwargs={'pk':'1'}),data)
        self.assertEqual(response.status_code,status.HTTP_202_ACCEPTED)
    
    # Team member can modify only status field using PATCH
    def test_partial_update_by_member_status_field(self):
        self.client.force_authenticate(user=self.member1)
        response = self.client.patch(reverse('task-detail',kwargs={'pk': '1'}),{'status': 'In Progress'})
        self.assertEqual(response.status_code,status.HTTP_202_ACCEPTED)
    
    def test_partial_update_by_member_restricted_field(self):
        self.client.force_authenticate(user=self.member1)
        response = self.client.patch(reverse('task-detail',kwargs={'pk': '1'}),{'name': 'Another job'})
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
    
    # leader can modify any field with PATCH
    def test_partial_update_by_leader_any_field(self):
        self.client.force_authenticate(user=self.leader1)
        response = self.client.patch(reverse('task-detail',kwargs={'pk': '1'}),{'name': 'New Name'})
        self.assertEqual(response.status_code,status.HTTP_202_ACCEPTED)
    



    
    
    

