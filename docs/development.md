# Development

## Requirements - Local Env

* MySQL
* Docker

## Setup

```shell
# Create the DB
cd django
python3 manage.py migrate
```

## Dev Local Env

```shell
cd django
docker build . -t phippy
docker run -p 8000:8000 --name phippy --rm -it -v $PWD/:/code phippy
```
