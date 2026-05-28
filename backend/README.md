# 🚀 Setup — FastAPI Multitenant Kiosk

## Pré-requisitos

- Python 3.11+
- PostgreSQL instalado e rodando

---

## 1. Ambiente virtual

### Linux / macOS
```bash
python -m venv .venv
source .venv/bin/activate
```

### Windows
```bash
python -m venv .venv
.venv\Scripts\activate
```

---

## 2. Instalar dependências

```bash
pip install -r requirements.txt
```

---

##  Arquivo `.env`

Crie um arquivo `.env` na pasta do backend com as seguintes variaveis:

```env
DATABASE_URL=postgresql+asyncpg://usuario:senha@localhost:5432/nome_do_banco
JWT_SECRET_KEY=sua_chave_secreta
APP_DEBUG=true
```

> Substitua `usuario`, `senha` e `nome_do_banco` pelos dados do seu PostgreSQL.


##  Rodar o servidor

```bash
uvicorn app.main:app --reload
```

Acesse a documentação em: [http://localhost:8000/docs](http://localhost:8000/docs)
