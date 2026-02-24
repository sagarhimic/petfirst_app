# app/routers/customers/cart.py
from fastapi import APIRouter, Depends, Form, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.jwt_auth import get_auth_user_id
from app.services.customers.cart_service import add_to_cart_service, cart_details_service, remove_service_by_cart, clear_cart_service


async def add_to_cart(
    request: Request,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_auth_user_id)
):
    form = await request.form()

    return add_to_cart_service(
        db=db,
        user_id=user_id,
        form=form
    )

def cart_details(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_auth_user_id)
):
    return cart_details_service(db, user_id)

def remove_service(
    service_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_auth_user_id)
):
    return remove_service_by_cart(db, user_id, service_id)

def clear_cart(
    trainer_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_auth_user_id)
):
    return clear_cart_service(db, user_id, trainer_id)
