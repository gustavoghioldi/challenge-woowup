Woowup Challenge Backend
===========

[Documentación](https://2trdeh54hp.apidog.io/doc-664088)

Correr en local
===============
```$ docker compose up --build```

Documentación técnica
=====================
1 - Variables de ambiente:
- SECRET_KEY = Llave de encriptación (String)
- DEBUG = 1 -No setar para modo productivo- (Integer)
- REDIS_LOCATION = host de redis
- DJANGO_FIRST_PASSWORD = En el primer deploy crea un usuario de prueba (user: testuser, pass: DJANGO_FIRST_PASSWORD o "testpassword", si no se setea la variable)
