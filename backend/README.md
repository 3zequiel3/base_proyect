# Backend

Backend base con **FastAPI**, **SQLModel**, **PostgreSQL** y una estructura simple pensada para reutilizarse en forks.

## Stack

- FastAPI
- SQLModel
- SQLAlchemy async
- PostgreSQL
- Pydantic Settings
- Uvicorn

## Estructura

```txt
backend/
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── basemodel.py
│   │   ├── baserepository.py
│   │   ├── baseservice.py
│   │   ├── baseuow.py
│   │   ├── database.py
│   │   └── settings_database.py
│   └── modules/
│       └── .gitkeep
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## Flujo de arquitectura

El flujo base del backend es:

```txt
Router -> Service -> UnitOfWork -> Repository -> Model/DB
```

- **Router**: recibe requests HTTP y llama al service correspondiente.
- **Service**: coordina el caso de uso y abre el `UnitOfWork`.
- **UnitOfWork**: maneja sesión, commit, rollback, close y refresh.
- **Repository**: encapsula el CRUD contra la base de datos.
- **Model**: entidades SQLModel persistidas en PostgreSQL.

## Core

### `main.py`

Entry point de FastAPI.

Incluye:

- `FastAPI(...)`
- `lifespan`
- endpoint `GET /health`
- creación opcional de DB/tablas según `.env`
- cierre del engine al apagar la app

### `core/settings_database.py`

Define la configuración con `pydantic-settings`.

Lee variables desde:

```txt
backend/.env
```

Variables principales:

- `APP_NAME`
- `APP_VERSION`
- `DB_USER`
- `DB_PASSWORD`
- `DB_HOST`
- `DB_PORT`
- `DB_NAME`
- `DB_ECHO`
- `DB_CREATE_DATABASE`
- `DB_CREATE_TABLES`
- `DATABASE_URL`

### `core/database.py`

Configura la conexión a PostgreSQL.

Expone:

- `engine`
- `SessionLocal`
- `create_database_if_not_exists()`
- `create_db_and_tables()`
- `dispose_engine()`
- `get_session()`

### `core/basemodel.py`

Modelo base para entidades SQLModel.

Incluye:

- `id` entero autoincremental compatible con PostgreSQL `BIGSERIAL`
- `created_at`
- `updated_at`
- `deleted_at`
- `mark_deleted()` para soft delete

### `core/baseuow.py`

Unit of Work simple.

Responsabilidades:

- abre sesión al entrar
- hace `commit` si no hay error
- hace `rollback` si hay error
- cierra la sesión siempre
- expone `refresh()`

### `core/baserepository.py`

Repositorio genérico CRUD.

Métodos:

- `add()`
- `create()`
- `get_by_id()`
- `list_active()`
- `update()`
- `delete()`

`list_active()` devuelve solo registros con `deleted_at IS NULL`.

`delete()` realiza soft delete.

### `core/baseservice.py`

Service genérico CRUD.

Métodos:

- `create()`
- `get_by_id()`
- `list_active()`
- `update()`
- `delete()`

## Convención para módulos

Cada módulo dentro de `app/modules/` debería tener sus propios archivos.

Ejemplo:

```txt
app/modules/users/
├── __init__.py
├── models.py
├── repository.py
├── service.py
├── schemas.py
└── router.py
```

Ejemplo de modelo:

```python
from sqlmodel import Field

from app.core.basemodel import BaseModel


class User(BaseModel, table=True):
    name: str = Field(index=True)
    email: str = Field(unique=True, index=True)
```

Ejemplo de repository:

```python
from app.core.baserepository import BaseRepository
from app.modules.users.models import User


class UserRepository(BaseRepository[User]):
    model = User
```

Ejemplo de service:

```python
from app.core.baseservice import BaseService
from app.core.baseuow import UnitOfWork
from app.modules.users.models import User
from app.modules.users.repository import UserRepository


class UserService(BaseService[User, UserRepository]):
    def __init__(self, uow: UnitOfWork):
        super().__init__(uow, UserRepository)
```

## Configuración local

Copiar el template:

```bash
cp .env.example .env
```

Editar las variables de PostgreSQL según el entorno.

## Instalación

Desde `backend/`:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecución

Desde `backend/`:

```bash
uvicorn app.main:app --reload
```

Healthcheck:

```txt
GET http://localhost:8000/health
```

## Notas

- Para desarrollo local se puede activar `DB_CREATE_DATABASE=true` y/o `DB_CREATE_TABLES=true`.
- Para producción se recomienda crear la base y manejar cambios de esquema con migraciones.
- Los archivos `.env` no se versionan; usar `.env.example` como referencia.
