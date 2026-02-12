# Orkestro | Menus, chatbot e análises.

### Tecnologias

<section align="left">
    <img alt="Static Badge" src="https://img.shields.io/badge/Python-grey?style=flat&logo=Python">
    <img alt="Static Badge" src="https://img.shields.io/badge/JavaScript-grey?style=flat&logo=JavaScript">
    <img alt="Static Badge" src="https://img.shields.io/badge/Flask-grey?style=flat&logo=Flask">
    <img alt="Static Badge" src="https://img.shields.io/badge/Flask--Marshmallow-grey?style=flat&logo=Flask">
    <img alt="Static Badge" src="https://img.shields.io/badge/Flask--SQLAlchemy-grey?style=flat&logo=Flask">
    <img alt="Static Badge" src="https://img.shields.io/badge/Flask--SocketIO-grey?style=flat&logo=Flask">
    <img alt="Static Badge" src="https://img.shields.io/badge/Flask--Migrate-grey?style=flat&logo=Flask">
    <img alt="Static Badge" src="https://img.shields.io/badge/HTML5-grey?style=flat&logo=HTML5">
    <img alt="Static Badge" src="https://img.shields.io/badge/Jinja-grey?style=flat&logo=Jinja">
    <img alt="Static Badge" src="https://img.shields.io/badge/JQuery-grey?style=flat&logo=JQuery">
    <img alt="Static Badge" src="https://img.shields.io/badge/TailwindCSS-grey?style=flat&logo=TailwindCSS">
    <img alt="Static Badge" src="https://img.shields.io/badge/PyTest-grey?style=flat&logo=PyTest">
    <img alt="Static Badge" src="https://img.shields.io/badge/Docker-grey?style=flat&logo=Docker">
    <img alt="Static Badge" src="https://img.shields.io/badge/Docker Compose-grey?style=flat&logo=Docker">
    <img alt="Static Badge" src="https://img.shields.io/badge/PostgreSQL-grey?style=flat&logo=PostgreSQL">
    <img alt="Static Badge" src="https://img.shields.io/badge/PgAdmin-grey?style=flat&logo=PostgreSQL">
    <img alt="Static Badge" src="https://img.shields.io/badge/Supabase-grey?style=flat&logo=Supabase">
    <img alt="Static Badge" src="https://img.shields.io/badge/Redis-grey?style=flat&logo=Redis">
    <img alt="Static Badge" src="https://img.shields.io/badge/Postman-grey?style=flat&logo=Postman">
    <img alt="Static Badge" src="https://img.shields.io/badge/N8N-grey?style=flat&logo=N8N">
    <img alt="Static Badge" src="https://img.shields.io/badge/Makefile-grey?style=flat&logo=Make">
</section>

## Descrição
A complete web app for intelligent menu management, combining chatbot automation to enhance customer interaction and advanced analytics to drive smarter decisions.

## How to start the project
To initialize the project, the following technologies are essential:
- Python installed (version >= 3.12.3 is used in the project.)
- Docker and Docker Compose
- IDE of your choice (we chose PyCharm)
- Makefile for automation

Clone the project repository
```bash
$ https://github.com/flux-mind/orkestro.git
$ cd ./orkestro
```
Create a virtual environment
```bash
# Linux / macOS
$ python3 -m venv venv
$ source venv/bin/activate

# Windows
$ python -m venv venv
$ venv\Scripts\activate
```
Install all project dependencies
```bash
$ pip install -r ./source/requirements.txt
```
Now you must configure the necessary variables that are found in the directory `./source/docker/compose/.env.template`. Configure this `.env.template` and change it to `.env`
```bash
## DATABASE POSTGRESQL ##
DATABASE_HOST=
DATABASE_PORT=
DATABASE_NAME=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=

## PGADMIN ##
PGADMIN_DEFAULT_EMAIL=
PGADMIN_DEFAULT_PASSWORD=
PGADMIN_HOST=
PGADMIN_PORT=

## REDIS ##
REDIS_HOST=
REDIS_PORT=
```
> **Notes:**
> - These settings are of utmost importance, if you experience any difficulties, we recommend consulting one of the maintainers.


At the root of the directory, initialize all necessary containers
```bash
$ make up
```
After these steps, your project will be available at the url defined by you (this depends on the environment variables)
```bash
http://localhost:port
```

## How to contribute

## Documentation

### API Swagger

### Web Docs

