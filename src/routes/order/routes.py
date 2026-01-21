from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse

from src.db.depencies import get_db
from src.db.models.models import Order, Product, OrderItem
from src.schemas.order.schema import OrderModel

order_router = APIRouter()

@order_router.post('/create')
def create_order(order_data: OrderModel, db:Session = Depends(get_db)):
    try:
        # get order by id
        order = db.query(Order).where(Order.id == order_data.id).scalar()
        # get product by id
        product = db.query(Product).where(Product.id == order_data.product_id).scalar()
        # check exists order
        if order == None:
            return HTTPException(status_code=404, detail=f"Order %{order_data.id} not found!")

        if product == None:
            return HTTPException(status_code=404, detail=f"Product %{order_data.product_id} not found!")

        order_item = db.query(OrderItem).where(OrderItem.product_id == order_data.product_id).where(OrderItem.order_id == order_data.id).first()

        if order_item == None:
            new_order_item = OrderItem(order_id=order_data.id, product_id=order_data.product_id, quantity=order_data.quantity)
            db.add(new_order_item)
            order.append(new_order_item)
            db.commit()
        else:
            print(f"order_data.quantity={order_data.quantity}")
            print(f"before update quantity={order_item.quantity}")
            order_item.quantity = order_data.quantity
            print(f"after update quantity={order_item.quantity}")
        
        order.set_total_price(order_data.quantity)
    except Exception as error:
        db.rollback()
        return HTTPException(status_code=error)
    else:
        db.commit()

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=jsonable_encoder(order_data)
    )
