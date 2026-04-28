# Frontend Storefront (Angular 17)

Frontend del sistema e-commerce construido con Angular 17 (standalone APIs) y estructura por dominios para facilitar crecimiento del producto.

## Principios aplicados

- Separacion de responsabilidades: rutas, UI, seguridad y acceso HTTP desacoplados.
- Escalabilidad: lazy loading por features (`auth`, `catalog`, `orders`).
- Seguridad cliente: interceptor de JWT + guard de rutas privadas.
- Manejo de errores: interceptor centralizado para 401/5xx y mensajes consistentes.
- Mantenibilidad: `core` para capacidades transversales y `features` para negocio.

## Estructura

```text
src/app/
	core/
		constants/
		guards/
		interceptors/
		models/
		services/
	features/
		auth/
		catalog/
		orders/
	app.config.ts
	app.routes.ts
```

## Seguridad y errores

- `auth.interceptor.ts`: agrega `Authorization: Bearer <token>`.
- `http-error.interceptor.ts`: centraliza manejo de errores HTTP y expiracion de sesion.
- `auth.guard.ts`: protege rutas privadas.
- `auth-token.service.ts`: encapsula persistencia de token.

## Desarrollo local

```bash
npm run start
```

Aplicacion disponible en `http://localhost:4200`.

## Integracion con backend

La URL base de API esta en `src/app/core/constants/api.constants.ts`:

- `API_BASE_URL = http://localhost:8000/api/v1`

Si cambias host/puerto, actualiza esta constante o migra a `environment.ts` por entorno.

## Scripts

- `npm run start`: servidor de desarrollo.
- `npm run build`: build de produccion.
- `npm run test`: pruebas unitarias.
