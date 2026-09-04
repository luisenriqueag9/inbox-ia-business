# PROJECT STATE

**Proyecto:** Inbox IA Business
**Version actual:** v0.0.3 — EN CURSO
**Fase actual:** Fase 1 / MVP

---

## Completado en v0.0.1

Establecer los cimientos técnicos y comprobar que frontend y backend pueden ejecutarse correctamente.

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
- Conexión FastAPI → PostgreSQL completada (SQLAlchemy 2.x + Psycopg 3).
- Alembic configurado y utilizando la conexión central del backend.
- Modelos iniciales multiempresa (Company y User) definidos en una única Base declarativa.
- Primera migración generada, validada (upgrade/downgrade exitoso) y aplicada en HEAD.

---

## Completado en v0.0.3 (hasta el momento)

- Preparación de sesiones SQLAlchemy mediante SessionLocal/get_db.
- Hashing seguro de contraseñas con Argon2 mediante pwdlib.
- Schemas Pydantic para registro y login.
- POST `/auth/register` (creación atómica de Company + User, detección de email duplicado, rollback).
- Modelo Session y migración Alembic correspondiente.
- Generación criptográficamente segura de tokens de sesión y almacenamiento del SHA‑256 del token.
- Autenticación de credenciales y rechazo de login para Company **SUSPENDED**.
- Creación de sesiones persistentes con duración de 7 días.
- Cookie HttpOnly `session` con SameSite=Lax; **Secure** configurable mediante `COOKIE_SECURE`.
- GET `/auth/me` con validación backend de sesión, expiración y estado de empresa.
- POST `/auth/logout` idempotente, invalida exclusivamente la sesión actual y elimina la cookie.
- Pruebas reales contra PostgreSQL validaron registro, login, `/auth/me`, logout, aislamiento entre dos sesiones del mismo usuario durante logout, rollback ante fallo de commit y comportamiento `COOKIE_SECURE` false/true.

---

## Problemas conocidos

- No hay problemas bloqueantes conocidos en la versión actual.

---

## Pendiente para próximas versiones

- Revisar alcance restante de v0.0.3 y decidir si la versión puede cerrarse.

---

## Fuera de Fase 1

- WhatsApp Business.
- Instagram.
- TikTok.
- Firebase.
- Respuestas automáticas mediante IA.