from typing import List
from datetime import date
from pydantic import BaseModel, Field, root_validator


class FinancialRecordBase(BaseModel):
    segment: str
    country: str
    product: str
    discount_band: str
    units_sold: float
    manufacturing_price: float
    sale_price: float
    gross_sales: float
    discounts: float
    sales: float
    cogs: float
    profit: float
    currency: str
    date: date
    month_number: int
    month_name: str
    year: int

class FinancialRecord(FinancialRecordBase):
    id: int

class FinancialRecordInDB(FinancialRecord):
    class Config:
        orm_mode = True
        fields_order = [
            "id",
            "segment",
            "country",
            "product",
            "discount_band",
            "units_sold",
            "manufacturing_price",
            "sale_price",
            "gross_sales",
            "discounts",
            "sales",
            "cogs",
            "profit",
            "currency",
            "date",
            "month_number",
            "month_name",
            "year",
        ]

    @root_validator
    def reorder(cls, values: dict) -> dict:
        return {field: values.get(field) for field in cls.Config.fields_order}
    
class FinancialRecordInCreate(FinancialRecordBase):
    pass

class FinancialRecordInUpdate(FinancialRecordBase):
    pass

class FinancialRecordsInDelete(BaseModel):
    ids: List[int]

class FinancialRecordsInResponse(BaseModel):
    success: bool
    data: List[FinancialRecordInDB] = None
    message: str = None

class FinancialRecordInResponse(BaseModel):
    success: bool
    data: FinancialRecordInDB = None
    message: str = None

    


    