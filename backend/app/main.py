from fastapi import FastAPI

app = FastAPI(title="Inbox IA Business API", version="0.0.1")


@app.get("/")
def root():
    return {"message": "Inbox IA Business API"}


@app.get("/health")
def health():
    return {"status": "ok"}
