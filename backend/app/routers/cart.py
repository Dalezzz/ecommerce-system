from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db.database import get_db
from ..schemas.cart import CartItemAdd, CartResponse
from ..services.cart_service import (
	agregar_item,
	limpiar_carrito,
	obtener_carrito_usuario,
	quitar_item,
	serializar_carrito,
)
from ..utils.security import get_current_user

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.get("/", response_model=CartResponse)
def get_my_cart(db: Session = Depends(get_db), user=Depends(get_current_user)):
	carrito = obtener_carrito_usuario(db, user.id)
	return serializar_carrito(carrito)


@router.post("/items", response_model=CartResponse)
def add_item(payload: CartItemAdd, db: Session = Depends(get_db), user=Depends(get_current_user)):
	carrito = agregar_item(db, user.id, payload.producto_id, payload.cantidad)
	return serializar_carrito(carrito)


@router.delete("/items/{producto_id}", response_model=CartResponse)
def remove_item(producto_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
	carrito = quitar_item(db, user.id, producto_id)
	return serializar_carrito(carrito)


@router.delete("/", response_model=CartResponse)
def clear_cart(db: Session = Depends(get_db), user=Depends(get_current_user)):
	carrito = limpiar_carrito(db, user.id)
	return serializar_carrito(carrito)
