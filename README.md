# OpenAwards

## Develop Environment

Create application (in OpenAwards/apps):

`python3 ../manage.py startapp openawards`

Update requirements:

`pip install -r OpenAwards/requirements/dev.txt`

Start DB server:

`$ sudo docker run -p 5432:5432 -e POSTGRES_PASSWORD=mysecretpassword postgres`

Connect to DB server and create DB:
```
$ export PGPASSWORD=mysecretpassword && psql -U postgres -h 127.0.0.1`
create database openawards;
```

```
python3 manage.py makemigrations
python3 manage.py migrate
```

`$ python manage runserver`