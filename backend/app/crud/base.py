from typing import Any, Generic, TypeVar

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database.base import Base


ModelType = TypeVar(
    "ModelType",
    bound=Base,
)

CreateSchemaType = TypeVar(
    "CreateSchemaType",
    bound=BaseModel,
)

UpdateSchemaType = TypeVar(
    "UpdateSchemaType",
    bound=BaseModel,
)


class CRUDBase(
    Generic[
        ModelType,
        CreateSchemaType,
        UpdateSchemaType,
    ]
):
    """
    Generic CRUD class.

    This class provides reusable database operations for
    every SQLAlchemy model in the project.
    """

    def __init__(
        self,
        model: type[ModelType],
    ):
        self.model = model

    def get(
        self,
        db: Session,
        record_id: int,
    ) -> ModelType | None:
        """
        Return one record by primary-key ID.
        """

        return db.get(
            self.model,
            record_id,
        )

    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> list[ModelType]:
        """
        Return multiple records with pagination.
        """

        statement = (
            select(self.model)
            .offset(skip)
            .limit(limit)
        )

        result = db.scalars(statement)

        return list(result.all())

    def create(
        self,
        db: Session,
        *,
        obj_in: CreateSchemaType,
    ) -> ModelType:
        """
        Create a new database record.
        """

        object_data = obj_in.model_dump()

        db_object = self.model(
            **object_data
        )

        try:
            db.add(db_object)
            db.commit()
            db.refresh(db_object)

            return db_object

        except IntegrityError:
            db.rollback()
            raise

        except Exception:
            db.rollback()
            raise

    def update(
        self,
        db: Session,
        *,
        db_object: ModelType,
        obj_in: UpdateSchemaType | dict[str, Any],
    ) -> ModelType:
        """
        Update an existing database record.

        Only explicitly provided fields are changed.
        """

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(
                exclude_unset=True
            )

        for field_name, value in update_data.items():
            if hasattr(db_object, field_name):
                setattr(
                    db_object,
                    field_name,
                    value,
                )

        try:
            db.add(db_object)
            db.commit()
            db.refresh(db_object)

            return db_object

        except IntegrityError:
            db.rollback()
            raise

        except Exception:
            db.rollback()
            raise

    def delete(
        self,
        db: Session,
        *,
        record_id: int,
    ) -> ModelType | None:
        """
        Delete a database record by ID.
        """

        db_object = self.get(
            db,
            record_id,
        )

        if db_object is None:
            return None

        try:
            db.delete(db_object)
            db.commit()

            return db_object

        except IntegrityError:
            db.rollback()
            raise

        except Exception:
            db.rollback()
            raise

    def exists(
        self,
        db: Session,
        *,
        record_id: int,
    ) -> bool:
        """
        Check whether a record exists.
        """

        return self.get(
            db,
            record_id,
        ) is not None

    def count(
        self,
        db: Session,
    ) -> int:
        """
        Return the total number of records.
        """

        statement = select(self.model)

        records = db.scalars(statement).all()

        return len(records)