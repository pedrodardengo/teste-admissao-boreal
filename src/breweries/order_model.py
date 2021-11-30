from pydantic import BaseModel


class Order(BaseModel):
    user: str
    order: float
    previous_order: bool
