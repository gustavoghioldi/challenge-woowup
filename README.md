Woowup Challenge Backend
===========

[Documentación](https://2trdeh54hp.apidog.io/doc-664088)

Run en local
===============
```$ docker compose up --build```

en caso de queres corre en local no virtualizado se debe tener instalado Postgres y redis, configurar las variables de ambiente y correr:

```
$ git clone git@github.com:gustavoghioldi/challenge-woowup.git
$ cd challenge-woowup
$ python3 -m venv .venv
$ source .venv/bin/activate 
$ pip install -r requirements.txt
$ python manage.py migrate
$ python manage.py createfirstuser
$ python manage.py deletecache

```
El primer usuario se setea con el comando createfirstuser y en el apartado de Variables de ambiente se explica como funciona en el docker-compose.yml ya se encuentra el comando en el pipeline. 

Variables de ambiente
=====================
- SECRET_KEY = Llave de encriptación (String)
- DEBUG = 1 -No setar para modo productivo- (Integer)
- REDIS_LOCATION = host de redis
- DATABASE_URL = ejemplo: "postgresql://myuser:mypassword@db:5432/mydatabase"
- DJANGO_FIRST_PASSWORD = En el primer deploy crea un usuario de prueba (user: testuser, pass: DJANGO_FIRST_PASSWORD o "testpassword", si no se setea la variable)
