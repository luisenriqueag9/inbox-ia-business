# Inbox IA Business

Version: **v0.0.1**

Sistema de bandeja de entrada inteligente para empresas.

## Requisitos previos

- Node.js >= 18
- Python >= 3.10
- npm >= 9

---

## Frontend (React + TypeScript + Vite)

### 1. Instalar dependencias

```bash
cd frontend
npm install
```

### 2. Ejecutar en modo desarrollo

```bash
npm run dev
```

La aplicacion estara disponible en http://localhost:5173

---

## Backend (Python + FastAPI + Uvicorn)

### 3. Crear y activar entorno virtual

```bash
cd backend

# Crear virtualenv
python -m venv .venv

# Activar en Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Activar en macOS / Linux
source .venv/bin/activate
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 5. Ejecutar FastAPI

```bash
uvicorn app.main:app --reload
```

La API estara disponible en http://localhost:8000

### 6. Verificar health check

```bash
curl http://localhost:8000/health
# o abrir en el navegador: http://localhost:8000/health
```

Respuesta esperada:

```json
{"status": "ok"}
```

---

## Variables de entorno

Copiar `.env.example` a `.env` cuando se requieran variables de entorno reales.
En v0.0.1 no es necesario.
