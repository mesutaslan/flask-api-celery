# restapi
Restful api example with Python Flask, SQLAlchemy, Celery and Redis

#### System requirements
````
Redis server, Python3.7, pip package installer
````

#### 1. Install packages
````
pip install --upgrade -r requirements.txt
````

#### 2. Create migration files and tables
````
- python migrate.py db init
- python migrate.py db migrate
- python migrate.py db upgrade
````               

#### 3. Run app 
````
export FLASK_APP=app.py
export FLASK_DEBUG=1
flask run
````

#### 4. Beat and Worker commands 
````
celery -A myapp.contacts.tasks.celery beat  --loglevel=info
celery -A myapp.contacts.tasks.celery worker  --loglevel=info
````

#### 5. Endpoints 
````
http://127.0.0.1:5000/api/contacts {GET,POST}
http://127.0.0.1:5000/api/contacts/<int:id> {GET,PUT,DELETE}
http://127.0.0.1:5000/contacts/<string:username> {GET}

http://127.0.0.1:5000/api/emails {GET,POST} 
http://127.0.0.1:5000/api/emails/<int:id> {GET,PUT,DELETE}
````

