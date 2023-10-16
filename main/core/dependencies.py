from fastapi import Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
)

from main.core.exceptions import (
    InactiveUserAccountException,
    FinancialRecordNotFoundException,
    UserPermissionException,
)
from main.db.repositories.financial_records import FinancialRecordsRepository, get_financial_records_repository
from main.models.financial_record import FinancialRecord
from main.models.user import User
from main.services.user import UserService

basic_security = HTTPBasic()


def get_current_user(
    user_service: UserService = Depends(),
    credentials: HTTPBasicCredentials = Depends(basic_security),
) -> User:
    """
    Return current user.
    """
    user = user_service.authenticate(
        username=credentials.username, password=credentials.password
    )
    return user


def get_current_financial_record(
    financial_record_id: str,
    repo: FinancialRecordsRepository = Depends(get_financial_records_repository),
    current_user: User = Depends(get_current_user),
) -> FinancialRecord:
    """
    Check if financial_record with `financial_record_id` exists in database.
    """
    financial_record = repo.get(obj_id=financial_record_id)
    if not financial_record:
        raise FinancialRecordNotFoundException(
            message=f"Financial Record with id `{financial_record_id}` not found",
            status_code=HTTP_404_NOT_FOUND,
        )
    if financial_record.owner_id != current_user.id:
        raise UserPermissionException(
            message="Not enough permissions", status_code=HTTP_403_FORBIDDEN
        )
    return financial_record


def get_current_active_user(
    user_service: UserService = Depends(),
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Return current active user.
    """
    if not user_service.check_is_active(user=current_user):
        raise InactiveUserAccountException(
            message="Inactive user", status_code=HTTP_400_BAD_REQUEST
        )
    return current_user
