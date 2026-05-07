# Frontend

Frontend base con **React**, **TypeScript**, **Vite** y **Tailwind CSS**.

La estructura está pensada para crecer por **features**, manteniendo separado lo compartido, la comunicación con APIs y el routing.

## Stack

- React
- TypeScript
- Vite
- Tailwind CSS
- ESLint
- pnpm

## Estructura actual

```txt
frontend/
├── public/
│   ├── favicon.svg
│   └── icons.svg
├── src/
│   ├── api/
│   │   └── .gitkeep
│   ├── assets/
│   │   ├── hero.png
│   │   ├── react.svg
│   │   └── vite.svg
│   ├── components/
│   │   ├── common/
│   │   │   └── .gitkeep
│   │   ├── layout/
│   │   │   └── .gitkeep
│   │   └── ui/
│   │       └── .gitkeep
│   ├── features/
│   │   └── example-feature/
│   │       ├── components/
│   │       │   └── .gitkeep
│   │       ├── hooks/
│   │       │   └── .gitkeep
│   │       ├── pages/
│   │       │   └── .gitkeep
│   │       ├── services/
│   │       │   └── .gitkeep
│   │       └── types/
│   │           └── .gitkeep
│   ├── lib/
│   │   ├── constants/
│   │   │   └── .gitkeep
│   │   ├── helpers/
│   │   │   └── .gitkeep
│   │   └── utils/
│   │       └── .gitkeep
│   ├── router/
│   │   └── .gitkeep
│   ├── App.tsx
│   ├── index.css
│   └── main.tsx
├── eslint.config.js
├── index.html
├── package.json
├── pnpm-lock.yaml
├── tsconfig.app.json
├── tsconfig.json
├── tsconfig.node.json
├── vite.config.ts
├── .gitignore
└── README.md
```

## Criterio de carpetas

### `src/main.tsx`

Punto de entrada de React. Monta la app en el DOM.

### `src/App.tsx`

Componente raíz.

Debería mantenerse liviano y delegar en:

- router
- layouts
- providers globales
- páginas principales

### `src/router/`

Configuración de rutas de la aplicación.

Ejemplos futuros:

```txt
src/router/
├── AppRouter.tsx
└── routes.tsx
```

### `src/api/`

Código compartido para comunicación HTTP.

Ejemplos futuros:

```txt
src/api/
├── client.ts
├── endpoints.ts
└── errors.ts
```

Uso esperado:

- configurar `fetch`/cliente HTTP
- manejar base URL
- interceptores o helpers comunes
- normalizar errores de API

### `src/components/`

Componentes compartidos por toda la app.

#### `components/ui/`

Componentes visuales reutilizables y de bajo nivel.

Ejemplos:

- `Button`
- `Input`
- `Modal`
- `Card`

#### `components/layout/`

Componentes de estructura.

Ejemplos:

- `MainLayout`
- `Sidebar`
- `Header`
- `Footer`

#### `components/common/`

Componentes comunes no necesariamente UI primitiva ni layout.

Ejemplos:

- `LoadingState`
- `EmptyState`
- `ErrorMessage`

### `src/features/`

Cada feature o módulo funcional vive en su propia carpeta.

Estructura base:

```txt
src/features/<feature-name>/
├── components/
├── hooks/
├── pages/
├── services/
└── types/
```

#### `features/<feature>/components/`

Componentes específicos de esa feature.

#### `features/<feature>/hooks/`

Hooks específicos de esa feature.

#### `features/<feature>/pages/`

Pantallas o páginas de esa feature.

#### `features/<feature>/services/`

Funciones que llaman a `src/api/` o encapsulan lógica de acceso a datos para esa feature.

#### `features/<feature>/types/`

Tipos TypeScript específicos de esa feature.

### `src/lib/`

Utilidades compartidas que no pertenecen a una feature concreta.

#### `lib/constants/`

Constantes globales.

#### `lib/helpers/`

Helpers de negocio o transformaciones reutilizables.

#### `lib/utils/`

Utilidades genéricas.

Ejemplos:

- formateo
- validaciones simples
- manejo de strings
- helpers de fechas

### `src/assets/`

Assets importados desde componentes React.

Ejemplos:

- imágenes
- SVGs
- recursos usados por componentes

### `public/`

Assets estáticos servidos directamente por Vite.

Ejemplos:

- favicon
- iconos públicos
- archivos estáticos que no pasan por el bundle

## Convenciones

- Lo compartido va en `components/`, `api/` o `lib/`.
- Lo específico de negocio va en `features/<feature>/`.
- Una feature no debería depender internamente de otra feature salvo que sea una decisión explícita.
- `App.tsx` y `main.tsx` deberían mantenerse simples.
- Los servicios de una feature deberían usar helpers comunes de `src/api/`.

## Variables de entorno

Vite solo expone variables que empiezan con:

```txt
VITE_
```

Ejemplo:

```env
VITE_API_URL=http://localhost:8000
```

Los `.env` reales no se versionan. Si se agrega un template, debe llamarse:

```txt
.env.example
```

## Instalación

Desde `frontend/`:

```bash
pnpm install
```

## Desarrollo

```bash
pnpm dev
```

## Build

```bash
pnpm build
```

## Lint

```bash
pnpm lint
```

## Preview de producción

```bash
pnpm preview
```

## Notas

- No versionar `node_modules/`.
- No subir `.env` reales.
- Mantener la estructura por features para evitar que `src/` se vuelva difícil de mantener.
- Los `.gitkeep` existen solo para conservar carpetas vacías en Git; se pueden borrar cuando haya archivos reales.
