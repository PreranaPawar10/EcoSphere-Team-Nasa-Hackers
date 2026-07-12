from app.crud.base import CRUDBase

from app.models import (
    Department,
    Category,
    EmissionFactor,
    ProductESGProfile,
    EnvironmentalGoal,
    ESGPolicy,
    Badge,
    Reward,
    CarbonTransaction,
    CSRActivity,
    EmployeeParticipation,
    Challenge,
    ChallengeParticipation,
    PolicyAcknowledgement,
    Audit,
    ComplianceIssue,
    DepartmentScore,
)

from app.schemas import (
    DepartmentCreate,
    DepartmentUpdate,
    CategoryCreate,
    CategoryUpdate,
    EmissionFactorCreate,
    EmissionFactorUpdate,
    ProductESGProfileCreate,
    ProductESGProfileUpdate,
    EnvironmentalGoalCreate,
    EnvironmentalGoalUpdate,
    ESGPolicyCreate,
    ESGPolicyUpdate,
    BadgeCreate,
    BadgeUpdate,
    RewardCreate,
    RewardUpdate,
    CarbonTransactionCreate,
    CarbonTransactionUpdate,
    CSRActivityCreate,
    CSRActivityUpdate,
    EmployeeParticipationCreate,
    EmployeeParticipationUpdate,
    ChallengeCreate,
    ChallengeUpdate,
    ChallengeParticipationCreate,
    ChallengeParticipationUpdate,
    PolicyAcknowledgementCreate,
    PolicyAcknowledgementUpdate,
    AuditCreate,
    AuditUpdate,
    ComplianceIssueCreate,
    ComplianceIssueUpdate,
    DepartmentScoreCreate,
    DepartmentScoreUpdate,
)


department_crud = CRUDBase[
    Department,
    DepartmentCreate,
    DepartmentUpdate,
](Department)


category_crud = CRUDBase[
    Category,
    CategoryCreate,
    CategoryUpdate,
](Category)


emission_factor_crud = CRUDBase[
    EmissionFactor,
    EmissionFactorCreate,
    EmissionFactorUpdate,
](EmissionFactor)


product_esg_profile_crud = CRUDBase[
    ProductESGProfile,
    ProductESGProfileCreate,
    ProductESGProfileUpdate,
](ProductESGProfile)


environmental_goal_crud = CRUDBase[
    EnvironmentalGoal,
    EnvironmentalGoalCreate,
    EnvironmentalGoalUpdate,
](EnvironmentalGoal)


esg_policy_crud = CRUDBase[
    ESGPolicy,
    ESGPolicyCreate,
    ESGPolicyUpdate,
](ESGPolicy)


badge_crud = CRUDBase[
    Badge,
    BadgeCreate,
    BadgeUpdate,
](Badge)


reward_crud = CRUDBase[
    Reward,
    RewardCreate,
    RewardUpdate,
](Reward)


carbon_transaction_crud = CRUDBase[
    CarbonTransaction,
    CarbonTransactionCreate,
    CarbonTransactionUpdate,
](CarbonTransaction)


csr_activity_crud = CRUDBase[
    CSRActivity,
    CSRActivityCreate,
    CSRActivityUpdate,
](CSRActivity)


employee_participation_crud = CRUDBase[
    EmployeeParticipation,
    EmployeeParticipationCreate,
    EmployeeParticipationUpdate,
](EmployeeParticipation)


challenge_crud = CRUDBase[
    Challenge,
    ChallengeCreate,
    ChallengeUpdate,
](Challenge)


challenge_participation_crud = CRUDBase[
    ChallengeParticipation,
    ChallengeParticipationCreate,
    ChallengeParticipationUpdate,
](ChallengeParticipation)


policy_acknowledgement_crud = CRUDBase[
    PolicyAcknowledgement,
    PolicyAcknowledgementCreate,
    PolicyAcknowledgementUpdate,
](PolicyAcknowledgement)


audit_crud = CRUDBase[
    Audit,
    AuditCreate,
    AuditUpdate,
](Audit)


compliance_issue_crud = CRUDBase[
    ComplianceIssue,
    ComplianceIssueCreate,
    ComplianceIssueUpdate,
](ComplianceIssue)


department_score_crud = CRUDBase[
    DepartmentScore,
    DepartmentScoreCreate,
    DepartmentScoreUpdate,
](DepartmentScore)