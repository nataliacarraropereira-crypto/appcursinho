# AppCursinho

Sistema web para gerenciar um cursinho preparatório para o vestibular da UFSC.

## Sobre o sistema

O sistema permite organizar:

- estudantes interessados
- professores responsáveis pelas aulas
- disciplinas ofertadas
- turmas disponíveis
- horários das aulas
- associação entre professores, disciplinas e turmas
- valores da mensalidade

A aplicação foi desenvolvida com Streamlit e SQLAlchemy, com suporte a SQLite para desenvolvimento local e MySQL para uso em produção.

## Tecnologias

- Python 3.11+
- Streamlit
- SQLAlchemy
- SQLite (desenvolvimento local)
- MySQL (produção)
- uv para gerenciamento de dependências e ambiente virtual

## Pré-requisitos

- Python 3.11+
- uv instalado

## Configuração do ambiente

1. Clone o repositório e entre na pasta do projeto.
2. Crie o ambiente virtual e instale as dependências:

```bash
uv sync
```

3. Configure as variáveis de conexão MySQL no arquivo `.env` local (o arquivo está no `.gitignore` e não deve ser compartilhado):

```dotenv
MYSQL_USER=seu_usuario
MYSQL_PASSWORD=sua_senha
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DATABASE=appcursinho
```

Também é possível configurar `MYSQL_DATABASE_URL` no ambiente de produção, por exemplo nos Secrets do Streamlit Community Cloud. Essa variável tem prioridade sobre as variáveis individuais. Se nenhuma configuração MySQL for definida, o sistema usa SQLite automaticamente para testes locais.

## Como executar

```bash
uv run streamlit run src/app.py
```

A aplicação estará disponível em http://localhost:8501.

## Estrutura do projeto

```text
appcursinho/
├── src/
│   ├── app.py
│   ├── db.py
│   ├── models.py
│   └── __init__.py
├── README.md
├── .gitignore
├── pyproject.toml
└── appcursinho.db (gerado automaticamente no SQLite)
```

## Observações de deploy

A aplicação foi pensada para ser implantada no Streamlit Community Cloud, seguindo a recomendação de deploy no ambiente oficial do Streamlit. Para produção, configure a variável de ambiente `MYSQL_DATABASE_URL` antes da execução.
