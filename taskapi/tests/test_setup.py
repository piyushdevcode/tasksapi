from rest_framework.test import APITestCase, force_authenticate
from rest_framework import status
from django.urls import reverse
from taskapi.models import *
# Create your tests here.

class TestSetUp(APITestCase):
    fixtures = ['test_data.json']
    def setUp(self):
        self.admin = User.objects.get(username='admin')
        self.user1 = User.objects.get(username='user1')
        self.user2 = User.objects.get(username='user2')
        self.leader1 = User.objects.get(username='leader1')
        self.leader2 = User.objects.get(username='leader2')
        self.member1 = User.objects.get(username='member1')
        self.member2 = User.objects.get(username='member2')
        self.team1 = Team.objects.get(pk=1)
        self.team2 = Team.objects.get(pk=2)

        return super().setUp()