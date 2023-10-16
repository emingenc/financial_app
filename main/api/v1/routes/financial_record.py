from typing import List

from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.params import Depends
from starlette.status import HTTP_201_CREATED

import pandas as pd

from main.core.dependencies import (
    basic_security,
    get_current_active_user,
    get_current_financial_record,
    get_current_user,
)
from main.db.repositories.financial_records import FinancialRecordsRepository, get_financial_records_repository
from main.models.financial_record import FinancialRecord
from main.models.user import User
from main.schemas.response import Response
from main.schemas.financial_records import FinancialRecordInCreate, FinancialRecordInDB, FinancialRecordInUpdate, FinancialRecordsInDelete

router = APIRouter(dependencies=[Depends(basic_security)])


@router.get("", response_model=Response[List[FinancialRecordInDB]])
def get_all_financial_records(
    skip: int = 0,
    limit: int = 20,
    financial_record_repo: FinancialRecordsRepository = Depends(get_financial_records_repository),
    current_user: User = Depends(get_current_user),
) -> Response:
    """
    Retrieve all financial_records.
    """
    financial_records = financial_record_repo.get_all_by_owner(
        owner_id=current_user.id, skip=skip, limit=limit
    )
    return Response(data=financial_records)


# export all data asynchronusly response model is only message and download csv file
@router.get("/export", response_class=FileResponse, response_model=Response[None])
async def export_all_data( financial_records_repo: FinancialRecordsRepository = Depends(get_financial_records_repository), current_user: User = Depends(get_current_active_user),) -> Response:
    """
    Export all data asynchronusly response model is only message and download csv file.
    """
    all_data= []
    while financial_records_repo.get_all_by_owner(
            owner_id=current_user.id, skip=len(all_data), limit=1000
        ) != []:
        all_data += financial_records_repo.get_all_by_owner(
            owner_id=current_user.id, skip=len(all_data), limit=1000
        )
    all_data = [financial_record.dict() for financial_record in all_data]
    
    df = pd.DataFrame(all_data)
    if df.empty:
        return Response(data=None, message="No data to export")
    
    df = df.drop(['id', 'owner_id'], axis=1)
    
    df.to_csv('export.csv', index=False)
    return FileResponse(path='export.csv', filename='export.csv', media_type='text/csv')


@router.get("/total_gross_sales", response_model=Response[float])
def get_total_gross_sales_by_segment(
    segment: str,
    currency: str,
    financial_record_repo: FinancialRecordsRepository = Depends(get_financial_records_repository),
    current_user: User = Depends(get_current_active_user),
) -> Response:
    """
    Get total gross sales by segment.
    """
    total_gross_sales = financial_record_repo.get_total_gross_sales_by_segment(segment=segment, currency=currency)
    print('x'*100)
    print(total_gross_sales)
    return Response(data=total_gross_sales)


@router.get("/{financial_record_id}", response_model=Response[FinancialRecordInDB])
def get_financial_record(financial_record: FinancialRecord = Depends(get_current_financial_record)) -> Response:
    """,
    Retrieve a financial_record by `financial_record_id`.
    """
    return Response(data=financial_record)


@router.post("", response_model=Response[FinancialRecordInDB], status_code=HTTP_201_CREATED)
def create_financial_record(
    financial_record: FinancialRecordInCreate,
    financial_records_repo: FinancialRecordsRepository = Depends(get_financial_records_repository),
    current_user: User = Depends(get_current_active_user),
) -> Response:
    """
    Create new financial_record.
    """
    financial_record = financial_records_repo.create_with_owner(obj_create=financial_record, owner_id=current_user.id)
    return Response(data=financial_record, message="The financial_record was created successfully")


@router.put("/{financial_record_id}", response_model=Response[FinancialRecordInDB])
def update_financial_record(
    financial_record_in_update: FinancialRecordInUpdate,
    financial_record: FinancialRecord = Depends(get_current_financial_record),
    financial_records_repo: FinancialRecordsRepository = Depends(get_financial_records_repository),
) -> Response:
    """
    Update financial_record by `financial_record_id`.
    """
    financial_record = financial_records_repo.update(obj=financial_record, obj_update=financial_record_in_update)
    return Response(data=financial_record, message="The financial_record was updated successfully")


@router.delete("/{financial_record_id}", response_model=Response[FinancialRecordInDB])
def delete_financial_record(
    financial_record: FinancialRecord = Depends(get_current_financial_record),
    financial_record_repo: FinancialRecordsRepository = Depends(get_financial_records_repository),
) -> Response:
    """
    Delete financial_record by `financial_record_id`.
    """
    financial_record = financial_record_repo.delete(obj_id=financial_record.id)
    return Response(data=financial_record, message="The financial_record was deleted successfully")


@router.delete("", response_model=Response[FinancialRecordsInDelete])
def delete_financial_records(
    financial_records: FinancialRecordsInDelete,
    financial_record_repo: FinancialRecordsRepository = Depends(get_financial_records_repository),
    current_user: User = Depends(get_current_active_user),
) -> Response:
    """
    Bulk delete financial_records.
    """
    financial_records = financial_record_repo.delete_many_by_owner(obj_ids=financial_records.ids, owner_id=current_user.id)
    return Response(
        data=FinancialRecordsInDelete(ids=financial_records), message="The financial_records was deleted successfully"
    )


# upload csv or xlsx file with financial_records
@router.post("/upload", response_model=Response[List[FinancialRecordInDB]], status_code=HTTP_201_CREATED)
def upload_financial_records(
    file: UploadFile = File(...),
    financial_records_repo: FinancialRecordsRepository = Depends(get_financial_records_repository),
    current_user: User = Depends(get_current_active_user),
) -> Response:
    """
    Upload csv or xlsx file with financial_records.
    """
    if file.content_type == "text/csv":
        df = pd.read_csv(file.file)
    elif file.content_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        df = pd.read_excel(file.file)
    else:
        return Response(data=None, message="File format is not supported")
    
    #drop emty rows
    df = df.dropna(how='all')

    # nan to None
    df = df.where(pd.notnull(df), None)

    obj_creates = df.to_dict("records")

    
    # lambda func
    preprocess_key = lambda key: key.strip().lower().replace(" ", "_")

    # strip if type is string
    preprocess_value = lambda val: val.strip() if type(val) == str else val
    
    # lowercase  and _ to space
    obj_creates = [{preprocess_key(k): preprocess_value(v) for k, v in obj_create.items()} for obj_create in obj_creates]

    financial_records = financial_records_repo.create_many_with_owner(obj_creates=obj_creates , owner_id=current_user.id)

    return Response(data=financial_records, message="The financial_records was created successfully")



