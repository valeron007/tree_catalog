from pydantic import BaseModel, field_validator


class OrderModel(BaseModel):
    id: int
    product_id: int
    quantity: int

    @field_validator('id')
    def check_id(cls, value: int) -> int:
        if value == None or value <= 0:
            raise ValueError('id must be at more 0')
        return value

    @field_validator('product_id')
    def check_product_id(cls, value: int) -> int:
        if value == None or value <= 0:
            raise ValueError('product_id must be at more 0')
        return value

    @field_validator('quantity')
    def check_quantity(cls, value: int) -> int:
        if value == None or value <= 0:
            raise ValueError('quantity must be at more 0')
        return value

