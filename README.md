# instructions

- create project: 
    $docker-compose run --rm blog django-admin.py startproject <PROJECT_NAME> . 
- create app: 
    $docker-compose run --rm blog python manage.py startapp <PROJECT_APP> 
- build app : 
    $docker-compose build 
- run app : 
    $docker-compose up

- create migrations:
    $ docker-compose run --rm blog python manage.py makemigrations
- migrate:
    $ docker-compose run --rm blog python manage.py migrate 

- db settings:
  - view images:
    $ docker ps
  - psql console:d
    $ docker exec -it <CONTAINER_ID>  psql -U postgres

  - psql:
   CREATE DATABASE <DB_NAME> WITH OWNER postgres ENCODING 'utf-8';

- test settings:
  - ngrok:
    https://dashboard.ngrok.com/get-started
    - install
      brew cask install ngrok
    - use
      ngrok http <PORT>