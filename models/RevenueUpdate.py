from pydantic import BaseModel


class RevenueUpdate(BaseModel):
    branch: str
    revenue_source: str
    revenue_category: str | None = None
    revenue_subcategory: str | None = None
    revenue_detail: str | None = None
    revenue_target: str | None = None
    week0: float | str | None = None
    week1: float | str | None = None
    week2: float | str | None = None
    week3: float | str | None = None
    week4: float | str | None = None
    week5: float | str | None = None
