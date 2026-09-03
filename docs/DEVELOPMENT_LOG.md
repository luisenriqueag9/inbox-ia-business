# Development Log — Inbox IA Business

## Dia 1 — v0.0.1

Fecha: 2026-09-03

### Objetivo

Establecer una base minima y comprobable para Inbox IA Business antes de implementar funcionalidades de negocio.

### Construido

- Estructura inicial del repositorio.
- Frontend con React + TypeScript + Vite.
- Backend con Python + FastAPI.
- Endpoint `GET /`.
- Endpoint `GET /health`.
- Configuracion inicial de `.gitignore`.
- `.env.example` sin secretos.
- README con instrucciones de ejecucion.
- PROJECT_STATE.md.
- DECISIONS.md.

### Arquitectura actual

```
Frontend (React + TypeScript)
  → posteriormente consumira API REST
  → Backend (FastAPI)
```

Todavia no existe base de datos ni integracion de IA.

### Validaciones

- `npm run build`: correcto.
- Importacion/inicializacion de FastAPI: correcta.
- `GET /health`: HTTP 200 con `{"status":"ok"}`.

### Decisiones importantes

- Mantener frontend y backend separados.
- Utilizar PostgreSQL posteriormente.
- Disenar multitenancy desde el modelo de datos.
- Validar autorizacion empresarial en backend.
- No exponer secretos en frontend.
- No implementar WhatsApp ni otras redes durante esta etapa.
- No permitir envio automatico de respuestas mediante IA en el MVP.

### Aprendizaje del dia

La primera version no busca tener funcionalidades comerciales todavia. Su proposito es establecer una base ejecutable y verificable sobre la que se puedan incorporar funcionalidades mediante cambios pequenos.

El proyecto se desarrolla incrementalmente: disenar → implementar → validar → revisar → documentar → commit.

### Estado al terminar el dia

v0.0.1 tecnicamente funcional y preparada para su primera version estable.

### Proximo paso

Inicializar/controlar correctamente el repositorio Git y crear el primer commit estable antes de comenzar v0.0.2.

---

## Dia 2 — v0.0.2

Fecha: 2026-09-03

### Objetivo

Incorporar PostgreSQL como base de datos de desarrollo local antes de implementar modelos de datos y logica de negocio.

### Completado

- Configuracion de Docker Compose con servicio PostgreSQL (`compose.yaml`).
- Actualizacion de `.env.example` con las variables requeridas por PostgreSQL.
- Infraestructura PostgreSQL validada manualmente (ver seccion Validaciones).
- Conexion FastAPI -> PostgreSQL implementada con SQLAlchemy 2.x y Psycopg 3.
- Endpoint `/health/db` para verificar disponibilidad de base de datos.
- Configuracion de Alembic en backend integrada con variables de entorno.
- Creacion de Base declarativa, modelo Company y modelo User.
- Generacion de primera migracion Alembic (`65c02fe1325e`).
- Correccion manual de migracion en downgrade() para eliminar el Enum PostgreSQL `companystatus`.
- Prueba completa de ciclo de migracion en entorno local.

### Validaciones realizadas

- `docker compose config --quiet` finalizo correctamente con las variables configuradas.
- PostgreSQL 16.9 se levanto mediante `docker compose up -d`.
- El contenedor alcanzo estado `healthy` segun el healthcheck configurado con `pg_isready`.
- Se ejecuto `SELECT version();` correctamente desde el contenedor.
- Se creo una tabla temporal (`persistence_test`) y se inserto una fila para probar persistencia.
- Se ejecuto `docker compose down`, destruyendo el contenedor pero conservando el volumen `inbox_ia_postgres_data`.
- Se recreo el contenedor y se comprobo que el dato previo seguia existiendo.
- Se elimino la tabla temporal; `\dt` confirmo que la base quedo sin tablas de prueba.
- Conexion Psycopg directa: OK.
- Conexion mediante `app.database` (SQLAlchemy, `SELECT 1`): OK.
- `GET /health/db` devuelve HTTP 200 con `{"status":"ok","database":"reachable"}`.
- `GET /` y `GET /health` continuan funcionando correctamente (HTTP 200).
- Upgrade de migracion de Alembic: OK (tablas e hilos Enum creados).
- Downgrade de migracion a base: OK (tablas y Enum completamente revertidos).
- Upgrade de restauracion a head: OK. Estado de BD comprobado en `65c02fe1325e (head)`.

### Proximo paso

- Comenzar flujo de registro de usuarios y autenticacion.

### Decisiones de esta sesion

- Se fija PostgreSQL 16.9 para evitar cambios inesperados de version durante el desarrollo.
- El servicio se llama `db` para mantener nombres cortos y convencionales.
- Conflicto detectado con instalaciones de PostgreSQL local en puertos 5432 y 5433; se decidio mapear el contenedor Docker al puerto 5434 del host.
- Las credenciales se inyectan via variables de entorno; nunca se colocan valores reales en `compose.yaml`.
- El volumen Docker se nombra explicitamente (`inbox_ia_postgres_data`) para facilitar su identificacion y gestion.
- Se incluye healthcheck con `pg_isready` para garantizar que el servicio este listo antes de conectar el backend.
- `restart: unless-stopped` es adecuado para desarrollo local sin querer reinicio automatico permanente.
- `DATABASE_URL` se documenta en `.env.example` como variable de configuracion para proporcionar al backend la URL de conexion. El driver de conexion se configuro a `postgresql+psycopg://` internamente en SQLAlchemy.
