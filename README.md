# Orkestro: plataforma web para gerenciamento de cardápios

## Tecnologias
...

## Descrição
Uma aplicação web completa para gerenciamento inteligente de cardápios, combinando automação por chatbot para melhorar a interação com clientes e análises avançadas para orientar decisões mais inteligentes.

## Pré-requisitos
Para executar o projeto, as seguintes tecnologias são necessárias:

- Python instalado (a versão >= 3.12.3 é utilizada neste projeto)
- Docker e Docker Compose
- Uma IDE de sua preferência (PyCharm, VSCode)
- Make (para automação de tarefas em ambientes GNU/Linux)

Clone o repositório do projeto:
```bash
git clone git@github.com:TechAbraao/orkestro.git
cd ./orkestro
```
Crie o ambiente virtual (.venv):
```bash
# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```
Instale todas as dependências necessárias para desenvolvimento:
```bash
pip install -r ./source/requirements/requirements-dev.txt
```
Configure todas as variáveis de ambiente presente em `.env.template` e, após as configurações, renomeie para `.env`:
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


Na raíz do projeto, inicialize os containers Docker:
```bash
make up
```
Após isso, faça as migrations:
```bash
flask db upgrade
```

Após todas as etapas, acesse em:
```bash
http://localhost:<port>
```

## How to contribute

## Documentation

### API Swagger

### Web Docs

