from fastapi import APIRouter

from main.api.v1.routes import financial_record, status, user

router = APIRouter()

router.include_router(router=status.router, tags=["Status"], prefix="/status")
router.include_router(router=user.router, tags=["User"], prefix="/user")
router.include_router(router=financial_record.router, tags=["FinancialRecord"], prefix="/financial-record")
