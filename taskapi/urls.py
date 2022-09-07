from django.urls import path,include
from taskapi import views
from rest_framework import routers
from rest_framework.authtoken import views as restviews

router = routers.DefaultRouter()

# router.register(r'tasks',views.TaskViewSet)

# router.register(r'users',views.UserViewSet)

# router.register(r'teams',views.TeamViewSet)

user_detail = views.UserViewSet.as_view(
    {
        'get' : 'retrieve'
    }
)
user_list = views.UserViewSet.as_view(
    {
        'get' : 'list',
        'post' : 'create'
    }
)
team_detail = views.TeamViewSet.as_view({
    'get' : 'retrieve',
})
team_list = views.TeamViewSet.as_view({
    'get' : 'list',
    'post': 'create'
})

task_detail = views.TaskViewSet.as_view({
    'get' : 'retrieve',
    'put' : 'update',
    'patch': 'partial_update'
})
task_list = views.TaskViewSet.as_view({
    'get' : 'list',
    'post': 'create'
})

urlpatterns = [
    path('users/',user_list,name='user-list'),
    path('users/<int:pk>/',user_list,name='user-detail'),
    path('teams/',team_list,name='team-list'),
    path('teams/<int:pk>/',team_detail,name='team-detail'),
    path('tasks/',task_list,name='task-list'),
    path('tasks/<int:pk>/',task_detail,name='task-detail'),
    
]
# urlpatterns += [
#     path('',include(router.urls))
# ]
urlpatterns += [
    path('',views.root_API,name='api-root'),
    path('auth-token/', restviews.obtain_auth_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]