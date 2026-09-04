# Development Log — Inbox IA Business

## Dia 1 — v0.0.1

Fecha: 2026-09-03

### Objetivo

Establecer una base mínima y comprobable para Inbox IA Business antes de implementar funcionalidades de negocio.

### Construido

- Estructura inicial del repositorio.
- Frontend con React + TypeScript + Vite.
- Backend con Python + FastAPI.
- Endpoint `GET /`.
- Endpoint `GET /health`.
- Configuración inicial de `.gitignore`.
- `.env.example` sin secretos.
- README con instrucciones de ejecución.
- PROJECT_STATE.md.
- DECISIONS.md.

### Arquitectura actual

```
Front-end (React + TypeScript)
  → consumirá API REST
  → Backend (FastAPI)
```

Todavía no existe base de datos ni integración de IA.

### Validaciones

- `npm run build`: correcto.
- Importación/inicialización de FastAPI: correcta.
- `GET /health`: HTTP 200 con `{"status":"ok"}`.

### Estado al terminar el día

v0.0.1 técnicamente funcional y preparada para su primera versión estable.

---

## Dia 2 — v0.0.2

Fecha: 2026-09-03

### Objetivo

Incorporar PostgreSQL como base de datos de desarrollo local antes de implementar modelos de datos y lógica de negocio.

### Completado

- Configuración de Docker Compose con servicio PostgreSQL (`compose.yaml`).
- Actualización de `.env.example` con las variables requeridas por PostgreSQL.
- Infraestructura PostgreSQL validada manualmente (ver sección Validaciones).
- Conexión FastAPI → PostgreSQL implementada con SQLAlchemy 2.x y Psycopg 3.
- Endpoint `/health/db` para verificar disponibilidad de base de datos.
- Configuración de Alembic en backend integrada con variables de entorno.
- Creación de Base declarativa, modelo Company y modelo User.
- Generación de primera migración Alembic (`65c02fe1325e`).
- Corrección manual de migración en downgrade() para eliminar el Enum PostgreSQL `companystatus`.
- Prueba completa de ciclo de migración en entorno local.

### Validaciones realizadas

- `docker compose config --quiet` finalizó correctamente con las variables configuradas.
- PostgreSQL 16.9 se levantó mediante `docker compose up -d`.
- El contenedor alcanzó estado `healthy` según el healthcheck configurado con `pg_isready`.
- Se ejecutó `SELECT version();` correctamente desde el contenedor.
- Se creó una tabla temporal (`persistence_test`) y se insertó una fila para probar persistencia.
- Se ejecutó `docker compose down`, destruyendo el contenedor pero conservando el volumen `inbox_ia_postgres_data`.
- Se recreó el contenedor y se comprobó que el dato previo seguía existiendo.
- Se eliminó la tabla temporal; `\dt` confirmó que la base quedó sin tablas de prueba.
- Conexión Psycopg directa: OK.
- Conexión mediante `app.database` (SQLAlchemy, `SELECT 1`): OK.
- `GET /health/db` devuelve HTTP 200 con `{"status":"ok","database":"reachable"}`.
- `GET /` y `GET /health` continúan funcionando correctamente (HTTP 200).
- Upgrade de migración de Alembic: OK (tablas y enum creados).
- Downgrade de migración a base: OK (tablas y enum completamente revertidos).
- Upgrade de restauración a head: OK. Estado de BD comprobado en `65c02fe1325e (head)`.

### Próximo paso

- Comenzar flujo de registro de usuarios y autenticación.

### Decisiones de esta sesión

- Se fija PostgreSQL 16.9 para evitar cambios inesperados de versión durante el desarrollo.
- El servicio se llama `db` para mantener nombres cortos y convencionales.
- Conflicto detectado con instalaciones de PostgreSQL local en puertos 5432 y 5433; se decidió mapear el contenedor Docker al puerto 5434 del host.
- Las credenciales se inyectan vía variables de entorno; nunca se colocan valores reales en `compose.yaml`.
- El volumen Docker se nombra explícitamente (`inbox_ia_postgres_data`) para facilitar su identificación y gestión.
- Se incluye healthcheck con `pg_isready` para garantizar que el servicio esté listo antes de conectar el backend.
- `DATABASE_URL` se documenta en `.env.example` como variable de configuración para proporcionar al backend la URL de conexión. El driver de conexión se configuró a `postgresql+psycopg://` internamente en SQLAlchemy.

---

## Dia 3 — v0.0.3 (en curso)

Fecha: 2026-09-03

### Objetivo

Implementar el registro de usuarios (Company + User) y preparar la base de datos para manejar sesiones.

### Completado

- Incorporación de pwdlib con Argon2 para el hashing seguro de contraseñas.
- Implementación de sesión de SQLAlchemy para requests (`get_db` / `SessionLocal`).
- Creación de schemas Pydantic para el registro con validaciones (ej. EmailStr).
- Implementación del endpoint `POST /auth/register`.
- Transacción atómica para la creación conjunta de `Company` y su primer `User`.
- Manejo de duplicados y errores de escritura (rollback y retornos 409).
- Elección de arquitectura de autenticación: sesiones opacas server‑side.
- Definición del modelo de base de datos `Session`.
- Generación de migración Alembic (`4369b716bb72_create_sessions.py`).
- Ciclo de validación exitoso: upgrade → downgrade → upgrade.
- Verificación de constraints `FK` y `UNIQUE` sobre la tabla de sesiones en PostgreSQL.
- Comprobación sin diferencias de `alembic check`.

### Próximo paso

- Implementar generación y hashing seguro del token de sesión.

---

## Dia 4 — v0.0.3 (autenticación)

Fecha: 2026-09-03

### Hitos de autenticación

- **Helpers de tokens seguros**: función `generate_session_token` con `secrets.token_urlsafe` y hash SHA‑256 mediante `hash_session_token`.
- **Schemas de login**: `LoginRequest` y `LoginResponse` añadidos a `app.schemas`.
- **`authenticate_user`**: lógica de verificación de credenciales y estado de empresa (suspendida).
- **Creación de Session durante login**: generación de token, hash almacenado y cookie `session` HttpOnly con SameSite=Lax, duración 7 días, `Secure` configurable mediante `COOKIE_SECURE`.
- **Configuración `COOKIE_SECURE`**: uso de `app.config.get_cookie_secure()` para decidir la bandera `secure` en la cookie.
- **`get_current_user`**: validación de sesión, expiración y estado de empresa.
- **GET `/auth/me`**: endpoint implementado, devuelve datos de empresa y usuario.
- **POST `/auth/logout`**: idempotente, elimina exclusivamente la sesión actual y envía `delete_cookie`.
- **Validación final con PostgreSQL real**: pruebas reales contra PostgreSQL confirmaron registro, login, `/auth/me`, logout, aislamiento de sesiones, rollback de commit y comportamiento `COOKIE_SECURE` false/true.
- **Intento descartado con SQLite**: se probó inicialmente con SQLite, se abortó y el repositorio se restauró; la validación final se realizó contra PostgreSQL.

---

## Próximos pasos

- Revisar alcance restante de v0.0.3 y decidir si la versión puede cerrarse.
