from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status,
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database.db import get_db

from app.schemas import (
    CarbonTransactionCreate,
    CarbonTransactionResponse,
    ChallengeParticipationCreate,
    ChallengeParticipationResponse,
    ComplianceIssueResponse,
    CSRActivityResponse,
    DepartmentScoreCreate,
    DepartmentScoreResponse,
    EmployeeParticipationCreate,
    EmployeeParticipationResponse,
)

from app.services import (
    carbon_service,
    challenge_participation_business_service,
    compliance_service,
    csr_participation_service,
    department_esg_score_service,
    reward_business_service,
)


special_router = APIRouter()



# AUTOMATIC CARBON CALCULATION


@special_router.post(
    "/carbon-transactions/calculate",
    response_model=CarbonTransactionResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Carbon Transactions"],
    summary="Calculate and create carbon transaction",
)
def calculate_carbon_transaction(
    payload: CarbonTransactionCreate,
    db: Session = Depends(get_db),
):
    try:
        return carbon_service.create_transaction(
            db,
            payload,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error

    except IntegrityError as error:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Carbon transaction could not be created.",
        ) from error



# WEIGHTED ESG SCORE CALCULATION

@special_router.post(
    "/department-scores/calculate",
    response_model=DepartmentScoreResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Department Scores"],
    summary="Calculate weighted department ESG score",
)
def calculate_department_score(
    payload: DepartmentScoreCreate,
    db: Session = Depends(get_db),
):
    try:
        return department_esg_score_service.create_score(
            db,
            payload,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error

    except IntegrityError as error:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Department score could not be created.",
        ) from error



# CSR PARTICIPATION WITH EVIDENCE VALIDATION


@special_router.post(
    "/employee-participations/validate",
    response_model=EmployeeParticipationResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Employee Participations"],
    summary="Create CSR participation with evidence validation",
)
def create_validated_csr_participation(
    payload: EmployeeParticipationCreate,
    evidence_required: bool = Query(
        default=False,
        description="Require proof before participation is saved",
    ),
    db: Session = Depends(get_db),
):
    try:
        return csr_participation_service.create_participation(
            db,
            payload,
            evidence_required=evidence_required,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error

    except IntegrityError as error:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="CSR participation could not be created.",
        ) from error



# CHALLENGE PARTICIPATION AND XP

@special_router.post(
    "/challenge-participations/validate",
    response_model=ChallengeParticipationResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Challenge Participations"],
    summary="Create challenge participation and calculate XP",
)
def create_validated_challenge_participation(
    payload: ChallengeParticipationCreate,
    db: Session = Depends(get_db),
):
    try:
        return (
            challenge_participation_business_service
            .create_participation(
                db,
                payload,
            )
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error

    except IntegrityError as error:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Challenge participation could not be created.",
        ) from error



# OVERDUE COMPLIANCE ISSUES


@special_router.get(
    "/compliance-issues/overdue",
    response_model=list[ComplianceIssueResponse],
    tags=["Compliance Issues"],
    summary="Get overdue compliance issues",
)
def get_overdue_compliance_issues(
    db: Session = Depends(get_db),
):
    return compliance_service.get_overdue_issues(db)



# REWARD VALIDATION


@special_router.get(
    "/rewards/{reward_id}/validate-redemption",
    tags=["Rewards"],
    summary="Validate reward redemption",
)
def validate_reward_redemption(
    reward_id: int,
    employee_points: int = Query(
        ge=0,
        description="Employee's current available points",
    ),
    db: Session = Depends(get_db),
):
    try:
        result = reward_business_service.validate_redemption(
            db,
            reward_id=reward_id,
            employee_points=employee_points,
        )

        reward = result["reward"]

        return {
            "valid": True,
            "reward_id": reward.id,
            "reward_name": reward.name,
            "points_required": reward.points_required,
            "current_stock": reward.stock,
            "remaining_points": result["remaining_points"],
        }

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error