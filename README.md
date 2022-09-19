# tasksapi
## How To Run
#### 1. Clone Repository
#### 2. install requirements using `pip install -r requirements.txt`
#### 3. run commands `python manage.py makemigrations` and `python manage.py migrate`
## To run tests
### start a celery worker `celery -A core -worker -l INFO`
### in the base directory run command `python manage.py test`

# API  
|End Point| HTTP Method | Result | Accessible by | 
|---------|-------------|--------|---------------|
|`auth-token/`| POST| get the authentication token | Anyone|
|`users/` | POST | create a new user | Admin|
|`users/` | GET  | list all users | Admin| 
|`users/<int:pk>/`|GET|retrieve specific user info | Admin |
|`teams/`| POST | create a new team | USER|
|`teams/`| GET | retrieve a team info| Authenticated User |
|`tasks/`| POST | create a new task | USER or Admin |
|`tasks/`| GET | list all the tasks | USER or Admin |
|`tasks/<int:pk>/`| POST | retrieve a task info | Member of Task |
|`tasks/<int:pk>/`| GET | retrieve a task info | Member of Task |
|`tasks/<int:pk/>`| PUT | Update task info(all fields) | Team Leader |
|`tasks/<int:pk/>`| PATCH | Update task info(only status field) | Team Member or Team Leader |


 


