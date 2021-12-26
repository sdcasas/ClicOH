Challenger ClicOH
==================


### Descripcion

Challenger ClicOH



## Intall

1. Creación de un entorno virtual.
2. Instalacion de dependencias: `pip install -r requirements/develop.txt`
3. Configuracion del proyecto desde el archivo `.env`: `cp src/env-example src/.env`
4. Crear estructura de la db. `python manage.py migrate`
5. Crear los archivos estaticos. `python manage.py collecstatic`