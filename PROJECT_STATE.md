# PROJECT STATE

**Proyecto:** Inbox IA Business
**Version actual:** v0.0.2
**Fase actual:** Fase 1 - MVP

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

## Pendiente para proximas versiones

- **SIGUIENTE TAREA:** Flujo de registro de usuarios y autenticacion inicial.
- Registro de usuarios (logica y endpoints).
- Autenticacion.
- Creacion de empresa.
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