# PROJECT STATE

**Proyecto:** Inbox IA Business
**Version actual:** v0.0.2 (en curso)
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

## En curso — v0.0.2

- PostgreSQL 16.9 para desarrollo local configurado y validado mediante Docker Compose (puerto host 5434).
  - Contenedor alcanza estado `healthy`.
  - Persistencia mediante volumen Docker verificada (`inbox_ia_postgres_data`).
- Conexion FastAPI -> PostgreSQL completada y validada (SQLAlchemy 2.x + Psycopg 3).
- Pendiente: configurar Alembic.
- Pendiente: definir modelos multiempresa iniciales.

---

## Pendiente para proximas versiones

- Modelo multiempresa (SQLAlchemy + Alembic).
- Registro de usuarios.
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
