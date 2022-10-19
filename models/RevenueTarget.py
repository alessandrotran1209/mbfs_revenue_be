from pydantic import BaseModel


class RevenueTarget(BaseModel):
    revenue_source: str
    revenue_category: str | None = None
    revenue_subcategory: str | None = None
    revenue_detail: str | None = None
    value: float | None = None
    branch: str | None = None
