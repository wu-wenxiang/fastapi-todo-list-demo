from typing import List, Optional

from sqlalchemy import delete, select, update

from todolist import db
from todolist.db import models


def todoelem_get_all(name: Optional[str] = None) -> List[models.Todoelem]:
    with db.DB_SESSION_LOCAL() as session:
        stmt = select(models.Todoelem)
        if name is not None:
            stmt = stmt.where(models.Todoelem.name.like(f"%{name}%"))
        result = session.execute(stmt).scalars().all()
        return result


def todoelem_get(todoelem_id: int) -> models.Todoelem:
    with db.DB_SESSION_LOCAL() as session:
        stmt = select(models.Todoelem).where(models.Todoelem.id == todoelem_id)
        result = session.execute(stmt).scalar_one()
        return result


def todoelem_create(todoelem: models.Todoelem) -> models.Todoelem:
    with db.DB_SESSION_LOCAL() as session:
        session.add(todoelem)
        session.commit()
        session.refresh(todoelem)
        return todoelem


def todoelem_bulk_create(todoelems: List[dict]) -> None:
    with db.DB_SESSION_LOCAL() as session:
        session.bulk_insert_mappings(models.Todoelem, todoelems)
        session.commit()


def todoelem_update(todoelem_id: int, todoelem: dict) -> models.Todoelem:
    with db.DB_SESSION_LOCAL() as session:
        stmt = update(models.Todoelem).where(models.Todoelem.id == todoelem_id).values(todoelem)
        session.execute(stmt)
        session.commit()
        todoelem = todoelem_get(todoelem_id)
        return todoelem


def todoelem_delete(todoelem_id: int) -> None:
    with db.DB_SESSION_LOCAL() as session:
        stmt = delete(models.Todoelem).where(models.Todoelem.id == todoelem_id)
        session.execute(stmt)
        session.commit()
