# Orkestro @ FATEC-ZL


## Tecnologias

<section align="left">
    <img alt="Static Badge" src="https://img.shields.io/badge/Python-grey?style=flat&logo=Python">
    <img alt="Static Badge" src="https://img.shields.io/badge/JavaScript-grey?style=flat&logo=JavaScript">
    <img alt="Static Badge" src="https://img.shields.io/badge/JQuery-grey?style=flat&logo=JQuery">
    <img alt="Static Badge" src="https://img.shields.io/badge/Marshmallow-grey?style=flat&logo=Python">
    <img alt="Static Badge" src="https://img.shields.io/badge/Jinja-grey?style=flat&logo=Jinja">
    <img alt="Static Badge" src="https://img.shields.io/badge/Flask-grey?style=flat&logo=Flask">
    <img alt="Static Badge" src="https://img.shields.io/badge/SQLAlchemy-grey?style=flat&logo=SQLAlchemy">
    <img alt="Static Badge" src="https://img.shields.io/badge/Docker-grey?style=flat&logo=Docker">
    <img alt="Static Badge" src="https://img.shields.io/badge/PostgreSQL-grey?style=flat&logo=PostgreSQL">
    <img alt="Static Badge" src="https://img.shields.io/badge/PgAdmin-grey?style=flat&logo=PostgreSQL">
    <img alt="Static Badge" src="https://img.shields.io/badge/Postman-grey?style=flat&logo=Postman">
    <img alt="Static Badge" src="https://img.shields.io/badge/Unittest-grey?style=flat&logo=Python">
    <img alt="Static Badge" src="https://img.shields.io/badge/Pytest-grey?style=flat&logo=Pytest">
    <img alt="Static Badge" src="https://img.shields.io/badge/TailwindCSS-grey?style=flat&logo=TailwindCSS">
    <img alt="Static Badge" src="https://img.shields.io/badge/Swagger (OpenAPI)-grey?style=flat&logo=Swagger">
    <img alt="Static Badge" src="https://img.shields.io/badge/Makefile-grey?style=flat&logo=Make">
</section>

## Descrição
- Orkestro é uma plataforma web de gerenciamento de cardápios desenvolvida para otimizar a rotina de pequenos comércios, centralizando a administração de produtos, preços e pedidos de forma simples e eficiente.

- Desenvolvido a partir dos conhecimentos adquiridos na Faculdade de Tecnologia da Zona Leste (FATEC-ZL), o projeto possui caráter acadêmico e busca simular práticas e processos utilizados em equipes reais de desenvolvimento de software.

## Pré-requisitos
Para executar o projeto, as seguintes tecnologias são necessárias:

- Python instalado (a versão >= 3.12.3 é utilizada neste projeto);
- Docker e Docker Compose;
- Uma IDE de sua preferência (PyCharm, VSCode);
- Make (para automação de tarefas em ambientes GNU/Linux).

## Rodar localmente
#### 1. Clone o repositório do projeto:
```bash
git clone git@github.com:TechAbraao/orkestro.git
cd ./orkestro
```
#### 2. Crie o ambiente virtual (.venv):
```bash
# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```
#### 3. Instale todas as dependências necessárias para desenvolvimento:
```bash
pip install -r ./source/requirements/requirements-dev.txt
```
#### 4. Configure todas as variáveis de ambiente presente em `.env.template` e, após as configurações, renomeie para `.env`:
```bash
FLASK_APP=source.app:create_app
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=[]
PYTHONPATH=$(pwd)
FLASK_HOST=localhost
FLASK_PORT=[]
DATABASE_HOST=[]
DATABASE_PORT=[]
DATABASE_NAME=[]
POSTGRES_USER=[]
POSTGRES_PASSWORD=[]
POSTGRES_DB=[]
PGADMIN_DEFAULT_EMAIL=[]
PGADMIN_DEFAULT_PASSWORD=[]
PGADMIN_HOST=[]
PGADMIN_PORT=[]
REDIS_HOST=[] 
REDIS_PORT=[]
ADMIN_EMAIL=[]
ADMIN_PASSWORD=[]
```
> **Notas:**
> - As configurações das variáveis de ambiente são de extrema importância para a inicialização do projeto. Em caso de dúvidas, consulte um dos mantenedores.


#### 5. Na raiz do projeto, inicialize os containers Docker:
```bash
make up
```
#### 6. Após isso, faça as migrations:
```bash
flask db upgrade
```

#### 7. Rode o projeto:
```bash
flask run 
```

#### 8. Disponível em:
```bash
http://localhost:<port>
```


