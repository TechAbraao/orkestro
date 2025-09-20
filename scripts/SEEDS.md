# Documentação dos Scripts de Banco de Dados

Este projeto fornece scripts Python para gerenciar e popular o banco de dados. Todos os scripts estão localizados no diretório `scripts/seeds/`.

## Visão Geral dos Scripts

| Script | Finalidade | Comando |
|--------|------------|---------|
| `clear_tables.py` | Apaga todos os registros de todas as tabelas, mantendo a estrutura das tabelas intacta. | `python3 -m scripts.seeds.clear_tables` |
| `seed_stores.py` | Popula a tabela `stores` com dados iniciais. Faz hash automático das senhas e define o `logo_url` padrão. | `python3 -m scripts.seeds.seed_stores` |
| `drop_all_tables.py` | Remove todas as tabelas do banco de dados. **Atenção:** Isso apagará todos os dados e a estrutura das tabelas. | `python3 -m scripts.seeds.drop_all_tables` |

## Observações
- Execute `clear_tables.py` antes de `seed_stores.py` se quiser iniciar com um banco de dados limpo.  
- Certifique-se de que sua aplicação Flask e as configurações do banco (`SQLALCHEMY_DATABASE_URI`) estão corretas.  
- Esses scripts exigem um **contexto de aplicação**, portanto sempre execute usando a forma de módulo (`python3 -m ...`).
