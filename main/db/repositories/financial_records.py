from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from main.core.config import get_app_settings
from main.db.repositories.base import BaseRepository
from main.db.session import get_db
from main.models.financial_record import FinancialRecord
from main.schemas.financial_records import FinancialRecordInCreate, FinancialRecordInUpdate
from main.utils.financial_records import preprocess_obj

import logging

settings = get_app_settings()


class FinancialRecordsRepository(BaseRepository[FinancialRecord, FinancialRecordInCreate, FinancialRecordInUpdate]):
    """
    Repository to manipulate with the FinancialRecordInUpdate.
    """

    def get_all_by_owner(
        self, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[FinancialRecord]:
        """
        Get all FinancialRecord created by specific user with id `owner_id`.
        """
        return (
            self.db.query(self.model)
            .filter(FinancialRecord.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create_with_owner(self, *, obj_create: FinancialRecordInCreate, owner_id: int) -> FinancialRecord:
        """
        Create new FinancialRecord by specific user with id `owner_id`.
        """
        obj = self.model(**obj_create.dict(), owner_id=owner_id)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete_many_by_owner(self, obj_ids: List[int], owner_id: int) -> List[int]:
        """
        Bulk delete objects.
        """
        query = (
            self.db.query(self.model)
            .filter(FinancialRecord.owner_id == owner_id)
            .filter(self.model.id.in_(obj_ids))
        )
        query.delete(synchronize_session=False)
        self.db.commit()
        return obj_ids
    
    def create_many_with_owner(self, *, obj_creates: List[FinancialRecordInCreate], owner_id: int) -> List[FinancialRecord]:
        """
        Create new FinancialRecordInDB by specific user with id `owner_id`.
        """
        obj_creates = list(map(preprocess_obj, obj_creates))
        objs = [self.model(**obj_create, owner_id=owner_id) for obj_create in obj_creates]
        self.db.add_all(objs)
        self.db.commit()
        print(objs)

        return objs
    
    #Oluşturulacak endpoint ile belirlenen segmente ait brüt satışların toplamı, belirlenen para biriminde  göster
    def get_total_gross_sales_by_segment(self, *, segment: str, currency: str) -> float:
        """
        Get all FinancialRecordInDB created by specific user with id `owner_id`.
        
        """
        # SELECT SUM(gross_sales)
        # FROM financial_record
        # WHERE segment = 'Government' AND currency = '$';
        # sqlalchmey ile yazılacak sum
        return self.db.query(func.sum(self.model.gross_sales)).filter(self.model.currency == '$').filter(self.model.segment == segment).scalar()

def get_financial_records_repository(session: Session = Depends(get_db)) -> FinancialRecordsRepository:
    return FinancialRecordsRepository(db=session, model=FinancialRecord)
