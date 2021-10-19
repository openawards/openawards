# OpenAwards

OpenAwards is a platform to remunerate all those artists, scientists, writers, and any kind of
creators who open their work to the world without asking for any payment.

OpenAwards uses a voting system to choose who and how should receive a prize.

## Prepare the develop environment

*⚠️ Please, remind to set a `DJANGO_SETTINGS_MODULE` environment variable pointing to a config
module that sets `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` ️ values.*

### Update requirements

Make sure you have pipenv installed and to initiate it in the project's folder.
If you are using PyCharm, use [this guide](https://www.jetbrains.com/help/pycharm/pipenv.html) to set everything up.

### Start a DB server

`sudo docker run -p 5432:5432 -e POSTGRES_PASSWORD=mysecretpassword -name postgres postgres`

Then you could connect to the DB server and create DB:
```
$ docker exec --user postgres postgres createdb openawards
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

```
apps/openawards/static/styles/scss$ sass --watch main.scss:../stylesheet.css
```

### Start a dev server

`$ python manage runserver`

### For production

You should add a new config file setting, at least, the next variables `DEBUG = False`,
`ALLOWED_HOSTS`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_STORAGE_BUCKET_NAME`,
and `SECRET_KEY`.

### Docker

Build the image on the root folder:

`$ env DJANGO_SETTINGS_MODULE=OpenAwards.settings.production docker-compose --file docker/docker-compose.yml build`

Run the app with (you should put the production.py settings file on OpenAwards/settings folder):

`$ env DJANGO_SETTINGS_MODULE=OpenAwards.settings.production docker-compose --file docker/docker-compose.yml up`

It will give an error due the DB 'openawards' has not been created yet. So the best option
is to log in into the db container and create it (to see the db container id: `$ docker ps`).
Then:

```
$ docker exec -ti <db container id> sh
$ env PGPASSWORD=mysecretpassword psql -h 127.0.0.1 -U postgres
postgres=# create database openawards;
```

After that you should migrate the db:

```
$ docker exec -ti <app container id> sh
$ python manage.py migrate
$ python manage.py collectstatic
```

You could also generate fake data with:

```
$ python manage.py generatefakedata
```

Or create the super user with:

```
$ python manage.py createsuperuser
```
=======================================================
NOTES OF ALFREDS to get running on local, october 2021:

Need to install dependencies with
```
pipenv install
```
start pipenv with:
```
pipenv shell
```
???

[2] You will need to start Postgres (in another terminal):
```
docker run --rm -p 5432:5432 -e POSTGRES_PASSWORD=mysecretpassword --name postgres postgres
```

[3] Create the Postgres database:
```
docker exec --user postgres postgres createdb openawards
```

[4] Create the database:
```
pipenv run python ./manage.py makemigrations
```

[5] Add the database structure in Postgres:
```
pipenv run python ./manage.py migrate
```

[6] Start the system:
```
pipenv run python ./manage.py runserver
```

The openawards should be up and running at: http://127.0.0.1:8000/

If you have problems it may be you already have a postgres installed. You can try in [3] :
```
sudo apt purge postgres
docker system prune -a
```
