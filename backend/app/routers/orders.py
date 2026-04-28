from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..db.database import get_db
from ..schemas.order import OrderCreate, OrderListResponse, OrderResponse
from ..services.order_service import (
	crear_orden_desde_carrito,
	cancelar_orden,
	detallar_orden,
	listar_ordenes,
	obtener_orden_por_id,
	reordenar_pedido,
)
from ..utils.security import get_current_user
from ..utils.security import require_admin

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/checkout", response_model=OrderResponse, status_code=201)
def checkout(payload: OrderCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
	return crear_orden_desde_carrito(db, user.id, payload, payload.metodo_pago)


@router.get("/mine", response_model=OrderListResponse)
def my_orders(
	estado: str | None = Query(default=None),
	pagina: int = Query(default=1, ge=1),
	tamano: int = Query(default=10, ge=1, le=100),
	orden: str = Query(default="desc"),
	db: Session = Depends(get_db),
	user=Depends(get_current_user),
):
	return listar_ordenes(db, usuario_id=user.id, estado=estado, pagina=pagina, tamano=tamano, orden_desc=orden != "asc")


@router.get("/", response_model=OrderListResponse)
def all_orders(
	estado: str | None = Query(default=None),
	pagina: int = Query(default=1, ge=1),
	tamano: int = Query(default=10, ge=1, le=100),
	orden: str = Query(default="desc"),
	db: Session = Depends(get_db),
	_=Depends(require_admin),
):
	return listar_ordenes(db, usuario_id=None, estado=estado, pagina=pagina, tamano=tamano, orden_desc=orden != "asc")


@router.get("/{order_id}", response_model=OrderResponse)
def order_detail(order_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
	orden = obtener_orden_por_id(db, order_id)
	role_value = getattr(user.rol, "value", str(user.rol))
	if orden.usuario_id != user.id and role_value != "admin":
		raise HTTPException(status_code=403, detail="Acceso denegado")
	return detallar_orden(db, orden)


@router.post("/{order_id}/reorder", response_model=dict)
def reorder(order_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
	return reordenar_pedido(db, user.id, order_id)


@router.post("/{order_id}/cancel", response_model=OrderResponse)
def cancel_order(order_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
	role_value = getattr(user.rol, "value", str(user.rol))
	return cancelar_orden(db, user.id, order_id, es_admin=role_value == "admin")
