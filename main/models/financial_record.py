from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from main.db.base_class import Base

class FinancialRecord(Base):
    __tablename__ = "financial_record"

    id = Column(Integer, primary_key=True, index=True)
    segment = Column(String, index=True)
    country = Column(String, index=True)
    product = Column(String, index=True)
    discount_band = Column(String, index=True)
    units_sold = Column(Float)
    manufacturing_price = Column(Float)
    sale_price = Column(Float)
    gross_sales = Column(Float)
    discounts = Column(Float)
    sales = Column(Float)
    cogs = Column(Float)
    profit = Column(Float)
    currency = Column(String, index=True)
    date = Column(Date, index=True)
    month_number = Column(Integer)
    month_name = Column(String, index=True)
    year = Column(Integer, index=True)
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="financial_records")

    def __init__(
        self,
        segment: str,
        country: str,
        product: str,
        discount_band: str,
        units_sold: int,
        manufacturing_price: float,
        sale_price: float,
        gross_sales: float,
        discounts: float,
        sales: float,
        cogs: float,
        profit: float,
        currency: str,
        date: Date,
        month_number: int,
        month_name: str,
        year: int,
        owner_id: int,
    ) -> None:
        self.segment = segment
        self.country = country
        self.product = product
        self.discount_band = discount_band
        self.units_sold = units_sold
        self.manufacturing_price = manufacturing_price
        self.sale_price = sale_price
        self.gross_sales = gross_sales
        self.discounts = discounts
        self.sales = sales
        self.cogs = cogs
        self.profit = profit
        self.currency = currency
        self.date = date
        self.month_number = month_number
        self.month_name = month_name
        self.year = year
        self.owner_id = owner_id


    def dict(self):
        return {
            "id": self.id,
            "segment": self.segment,
            "country": self.country,
            "product": self.product,
            "discount_band": self.discount_band,
            "units_sold": self.units_sold,
            "manufacturing_price": self.manufacturing_price,
            "sale_price": self.sale_price,
            "gross_sales": self.gross_sales,
            "discounts": self.discounts,
            "sales": self.sales,
            "cogs": self.cogs,
            "profit": self.profit,
            "currency": self.currency,
            "date": self.date,
            "month_number": self.month_number,
            "month_name": self.month_name,
            "year": self.year,
            "owner_id": self.owner_id,
        }

