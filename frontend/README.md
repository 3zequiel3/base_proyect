# Frontend

Frontend base con **React**, **TypeScript**, **Vite** y **Tailwind CSS**.

## Stack

- React
- TypeScript
- Vite
- Tailwind CSS
- ESLint
- pnpm

## Estructura

```txt
frontend/
├── public/
│   ├── favicon.svg
│   └── icons.svg
├── src/
│   ├── assets/
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

## Archivos principales

### `src/main.tsx`

Punto de entrada de React. Monta la aplicación en el DOM.

### `src/App.tsx`

Componente raíz de la aplicación.

En forks, desde acá se suele conectar:

- routing
- layout principal
- providers globales
- páginas iniciales

### `src/index.css`

Estilos globales.

También es el lugar base para importar/configurar Tailwind CSS.

### `vite.config.ts`

Configuración de Vite.

Actualmente define el plugin de React y la integración con Tailwind.

### `public/`

Assets estáticos servidos directamente por Vite.

Ejemplos:

- favicons
- iconos
- imágenes públicas

### `src/assets/`

Assets importados desde componentes React.

## Convención sugerida para crecer

Cuando el frontend empiece a crecer, se recomienda organizar por features o módulos.

Ejemplo:

```txt
src/
├── app/
│   ├── router.tsx
│   └── providers.tsx
├── shared/
│   ├── components/
│   ├── hooks/
│   ├── lib/
│   └── types/
├── modules/
│   └── users/
│       ├── components/
│       ├── pages/
│       ├── services/
│       └── types.ts
├── App.tsx
├── index.css
└── main.tsx
```

## Variables de entorno

Vite expone al frontend solo variables que empiezan con:

```txt
VITE_
```

Ejemplo recomendado:

```env
VITE_API_URL=http://localhost:8000
```

Si se agrega un `.env.example`, debe quedar versionado. Los `.env` reales están ignorados por `.gitignore`.

## Instalación

Desde `frontend/`:

```bash
pnpm install
```

## Ejecución

Desde `frontend/`:

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
- Mantener componentes compartidos en `shared/` cuando existan.
- Mantener lógica específica de negocio dentro de `modules/`.
