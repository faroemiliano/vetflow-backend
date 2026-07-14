from fastapi import APIRouter


router = APIRouter(
    tags=["Health"]
)


@router.get("/")
async def root():
    return {
        "message": "Bienvenido a VetFlow API 🐶🐱"
    }


@router.get("/health")
async def health():
    return {
        "status": "ok"
    }