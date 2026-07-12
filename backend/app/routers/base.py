from typing import Any

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    Response,
    status,
)
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.services.base import BaseService


def create_crud_router(
    *,
    service: BaseService,
    create_schema: type[BaseModel],
    update_schema: type[BaseModel],
    response_schema: type[BaseModel],
    prefix: str,
    tag: str,
    resource_name: str,
) -> APIRouter:
    """
    Create standard CRUD API endpoints for an entity.

    Generated endpoints:

    POST   /resource
    GET    /resource
    GET    /resource/{id}
    PATCH  /resource/{id}
    DELETE /resource/{id}
    """

    router = APIRouter(
        prefix=prefix,
        tags=[tag],
    )

    @router.post(
        "",
        response_model=response_schema,
        status_code=status.HTTP_201_CREATED,
        summary=f"Create {resource_name}",
    )
    def create_record(
        payload: create_schema,  # type: ignore[valid-type]
        db: Session = Depends(get_db),
    ) -> Any:
        try:
            return service.create(
                db,
                payload,
            )

        except IntegrityError as error:
            db.rollback()

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    f"{resource_name} could not be created. "
                    "A unique value may already exist, or a "
                    "foreign-key reference may be invalid."
                ),
            ) from error

        except ValueError as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(error),
            ) from error

    @router.get(
        "",
        response_model=list[response_schema],
        summary=f"List {resource_name} records",
    )
    def list_records(
        skip: int = Query(
            default=0,
            ge=0,
            description="Number of records to skip",
        ),
        limit: int = Query(
            default=100,
            ge=1,
            le=500,
            description="Maximum records to return",
        ),
        db: Session = Depends(get_db),
    ) -> Any:
        try:
            return service.list(
                db,
                skip=skip,
                limit=limit,
            )

        except ValueError as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(error),
            ) from error

    @router.get(
        "/{record_id}",
        response_model=response_schema,
        summary=f"Get {resource_name} by ID",
    )
    def get_record(
        record_id: int,
        db: Session = Depends(get_db),
    ) -> Any:
        record = service.get(
            db,
            record_id,
        )

        if record is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{resource_name} not found.",
            )

        return record

    @router.patch(
        "/{record_id}",
        response_model=response_schema,
        summary=f"Update {resource_name}",
    )
    def update_record(
        record_id: int,
        payload: update_schema,  # type: ignore[valid-type]
        db: Session = Depends(get_db),
    ) -> Any:
        try:
            updated_record = service.update(
                db,
                record_id,
                payload,
            )

            if updated_record is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"{resource_name} not found.",
                )

            return updated_record

        except HTTPException:
            raise

        except IntegrityError as error:
            db.rollback()

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    f"{resource_name} could not be updated. "
                    "A unique value may already exist, or a "
                    "foreign-key reference may be invalid."
                ),
            ) from error

        except ValueError as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(error),
            ) from error

    @router.delete(
        "/{record_id}",
        status_code=status.HTTP_204_NO_CONTENT,
        summary=f"Delete {resource_name}",
    )
    def delete_record(
        record_id: int,
        db: Session = Depends(get_db),
    ) -> Response:
        try:
            deleted_record = service.delete(
                db,
                record_id,
            )

            if deleted_record is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"{resource_name} not found.",
                )

            return Response(
                status_code=status.HTTP_204_NO_CONTENT
            )

        except HTTPException:
            raise

        except IntegrityError as error:
            db.rollback()

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    f"{resource_name} cannot be deleted "
                    "because other records reference it."
                ),
            ) from error

    return router