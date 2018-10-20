# OpenAwards

OpenAwards is a platform to remunerate all those artists, scientists, writers, and any kind of
creators who open their work to the world without asking for any payment. 

OpenAwards uses a voting system to choose who and how should receive a prize.

## Prepare the develop environment

*⚠️ Please, remind to set a `DJANGO_SETTINGS_MODULE` environment variable pointing to a config
module that sets `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` ️ values.*

### Update requirements

`pip install -r OpenAwards/requirements/dev.txt`

### Start a DB server

`$ sudo docker run -p 5432:5432 -e POSTGRES_PASSWORD=mysecretpassword postgres`

Then you could connect to the DB server and create DB:
```
$ export PGPASSWORD=mysecretpassword && psql -U postgres -h 127.0.0.1`
create database openawards;
```

### Create the DB structure
```
python3 manage.py makemigrations
python3 manage.py migrate
```

At this point you could add fake data (⚠ this action erases data in DB):
```
python3 manage.py generatefakedata
```
Probably you will need to add your AWS credentials into a settings module and launch it like:
```
env DJANGO_SETTINGS_MODULE=OpenAwards.settings.my_settings python manage.py generatefakedata
```


### Edit styles
CSS styles are coded in Sass, you need to compile the scss code:

```apps/openawards/static/styles/scss$ sass --watch main.scss:../stylesheet.css```

### Start a dev server

`$ python manage runserver`

### For production

You should add a new config file setting, at least, the next variables `DEBUG = False`, 
`ALLOWED_HOSTS`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_STORAGE_BUCKET_NAME`, 
and `SECRET_KEY`.