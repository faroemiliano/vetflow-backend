from fastapi import FastAPI

app = FastAPI(
    title="VeteFlow API",
    description="Api para sistema de gestion de veterinarias",
    version="1.0.0",
)

@app.get("/")
def root():
    return {"message": "Bienvenidos a  VeteFlow API!"}

@app.get("/health")
def health():
    return {"status": "ok"}