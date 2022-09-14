# tasksapi
## How To Run
#### 1. Clone Repository
#### 2. install requirements using `pip install -r requirements.txt`
#### 3. run commands `python manage.py makemigrations` and `python manage.py migrate`
## To run tests
### start a celery worker `celery -A core -worker -l INFO`
### in the base directory run command `python manage.py test`
