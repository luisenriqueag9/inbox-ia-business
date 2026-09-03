# PROJECT STATE

**Proyecto:** Inbox IA Business
**Version actual:** v0.0.3 — EN CURSO
**Fase actual:** Fase 1 / MVP

---

## Completado en v0.0.1

Establecer los cimientos tecnicos y comprobar que frontend y backend pueden ejecutarse correctamente.

- Estructura inicial del proyecto.
- Frontend React + TypeScript (Vite).
- Backend FastAPI.
- Endpoint de health check (`GET /health`).
- Frontend compila correctamente (`npm run build` sin errores).
- Backend FastAPI inicia e importa correctamente.
- `GET /health` verificado: HTTP 200 `{"status": "ok"}`.

---

## Completado en v0.0.2

- PostgreSQL 16.9 para desarrollo local configurado y validado mediante Docker Compose.
- Conexion FastAPI -> PostgreSQL completada (SQLAlchemy 2.x + Psycopg 3).
- Alembic configurado y utilizando la conexion central del backend.
- Modelos iniciales multiempresa (Company y User) definidos en una unica Base declarativa.
- Primera migracion generada, validada (upgrade/downgrade exitoso) y aplicada en HEAD.

---

## Completado en v0.0.3 (hasta el momento)

- Preparación de sesiones SQLAlchemy mediante SessionLocal/get_db.
- Hashing seguro de contraseñas con Argon2 mediante pwdlib.
- Schemas Pydantic para registro.
- POST `/auth/register`.
- Creación atómica de Company + primer User.
- Detección de email duplicado.
- Rollback ante errores de integridad/escritura.
- Modelo Session.
- Migración Alembic para sessions.
- Validación upgrade -> downgrade -> upgrade de migración.
- Alembic check limpio.
- Decisión de autenticación mediante sesiones opacas server-side persistidas en PostgreSQL y transportadas mediante cookie HttpOnly.

---

## Pendiente para proximas versiones

- **SIGUIENTE TAREA:** Implementar generación y hashing seguro del token de sesión.
- Generación criptográficamente segura del token de sesión.
- Hash determinista del token para token_hash.
- POST `/auth/login`.
- Creación/configuración de cookie HttpOnly.
- Autenticación de requests.
- Autorización/aislamiento multiempresa basado en usuario autenticado.
- POST `/auth/logout`.
- Frontend de registro/login.
- Mensajes manuales.
- Bandeja de entrada.
- Clasificacion mediante IA.
- Respuesta sugerida.
- Edicion de respuesta.
- Marcar conversacion como atendida.

---

## Fuera de Fase 1

- WhatsApp Business.
- Instagram.
- TikTok.
- Firebase.
- Respuestas automaticas mediante IA.