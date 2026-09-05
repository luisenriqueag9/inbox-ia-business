# PROJECT STATE

**Proyecto:** Inbox IA Business
**Version actual:** v0.0.4 — EN CURSO
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

## v0.0.3 – TERMINADA

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

## Problemas conocidos y consideraciones

A. **`Conversation.updated_at` y nuevos mensajes:** `updated_at` se actualiza cuando se modifica la fila `conversations`. Insertar un `Message` por sí solo NO implica que PostgreSQL/SQLAlchemy actualice automáticamente `Conversation.updated_at`. Al implementar nuevos mensajes/respuestas, la operación deberá tocar explícitamente la Conversation para que el orden de la bandeja refleje actividad reciente.

B. **Offset pagination:** Suficiente para el MVP. Cursor pagination queda como optimización futura si el volumen lo requiere.

C. **Índices actuales suficientes para esta etapa.** No crear índices compuestos todavía. Posibles índices futuros si la medición/query plans lo justifican:
   - `conversations(company_id, updated_at DESC, id DESC)`
   - `messages(conversation_id, created_at DESC, id DESC)`

D. **Desempate de último mensaje:** usa `created_at DESC, id DESC`. El UUID v4 sirve actualmente como desempate determinista, no como orden temporal. Si en el futuro se requiere orden exacto entre mensajes con timestamp idéntico, evaluar un campo explícito de secuencia/orden.

E. **Data temporal:** Puede existir data de pruebas anteriores que no fue posible identificar con certeza. No eliminar mediante borrados amplios.

---

## v0.0.4 – Mensajes y conversaciones manuales (TERMINADA)

Objetivo: crear la base mínima del dominio de Inbox IA Business para introducir conversaciones/mensajes manuales de prueba asociados a una empresa, con aislamiento estricto por `company_id`.

### Validado funcionalmente en v0.0.4

**Modelos y migración:**
- Modelos `Conversation` y `Message` validados en PostgreSQL real.
- `Conversation` pertenece a `Company` mediante `company_id`.
- `Message` pertenece a `Conversation`; tenancy derivado de Conversation, sin duplicar `company_id`.
- Reversibilidad probada: upgrade/downgrade/upgrade (incluye gestión de enums en PostgreSQL).
- Migración Alembic `1df139d55259_create_conversations_and_messages.py`.

**Aislamiento y Autenticación:**
- Aislamiento multiempresa implementado a nivel de backend.
- `company_id` derivado del usuario autenticado; el cliente no puede elegirlo.
- Empresas SUSPENDED bloqueadas centralmente (403).

**Endpoints de listado y creación:**
- `POST /conversations`: Conversation + primer Message INBOUND en transacción atómica.
- `GET /conversations`: Paginado (offset pagination aceptada para MVP).
- Bandeja ordenada `updated_at DESC, id DESC`.
- `last_message` resuelto eficientemente mediante `LEFT OUTER JOIN LATERAL`.
- Conversación sin mensajes soportada correctamente.

**Endpoints de detalle y actualización (NUEVOS):**
- `GET /conversations/{conversation_id}`: Filtra simultáneamente por `conversation_id` y `current_user.company_id`.
- Mensajes del detalle ordenados `created_at ASC, id ASC`.
- `PATCH /conversations/{conversation_id}/attended`: Operación ATTENDED idempotente.
- Segunda llamada ATTENDED no modifica `updated_at`.
- Rollback real de escritura validado empíricamente en PostgreSQL.

**Otros:**
- `/health` y `/health/db` funcionando correctamente.
- **Validación integrada final**: 22/22 pruebas PASS contra PostgreSQL real. Alembic current == head == 1df139d55259.

---

### Siguiente tarea

1. Cierre Git manual de v0.0.4:
   - commit
   - tag v0.0.4
   - push de main y tag

---

## Pendiente dentro de Fase 1 (Phase 1 NO terminada)

- Frontend funcional necesario para operar el MVP.
- Clasificación mediante IA.
- Detección de oportunidad comercial.
- Intención y prioridad.
- Respuesta sugerida.
- Edición humana de respuesta.

## Fuera de Fase 1

- WhatsApp Business real.
- Instagram.
- TikTok.
- Firebase / fuentes de conocimiento de fases posteriores.
- Envío automático mediante IA.
- Índices compuestos (no requeridos todavía).