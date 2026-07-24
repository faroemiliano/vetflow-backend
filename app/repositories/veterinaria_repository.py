from sqlalchemy.orm import Session

from app.models.veterinaria import Veterinaria


def get_veterinaria_by_slug(
    db: Session,
    slug: str,
):
    return (
        db.query(Veterinaria)
        .filter(
            Veterinaria.slug == slug
        )
        .first()
    )