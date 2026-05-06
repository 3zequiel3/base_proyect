# BaseProyecto

Proyecto base fullstack pensado para ser reutilizado en forks.

Incluye:

- Backend con FastAPI, SQLModel, PostgreSQL y estructura simple por módulos.
- Frontend con React, TypeScript, Vite y Tailwind CSS.

## Estructura general

```txt
.
├── backend/
│   ├── app/
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── README.md
├── .gitignore
└── README.md
```

## Documentación

- [Backend](./backend/README.md)
- [Frontend](./frontend/README.md)

## Flujo backend

```txt
Router -> Service -> UnitOfWork -> Repository -> Model/DB
```

El backend está preparado para crear módulos dentro de:

```txt
backend/app/modules/
```

## Desarrollo rápido

### Backend

```bash
cd backend
cp .env.example .env
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Healthcheck:

```txt
http://localhost:8000/health
```

### Frontend

```bash
cd frontend
pnpm install
pnpm dev
```

## Notas

- Los `.env` reales no se versionan.
- Los templates `.env.example` sí deben versionarse.
- Cada carpeta tiene su propio README con la estructura y convenciones específicas.
