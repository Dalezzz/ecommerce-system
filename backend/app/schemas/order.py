from datetime import datetime
from typing import List

from pydantic import BaseModel


class OrderCreate(BaseModel):
	direccion: str
	ciudad: str
	codigo_postal: str | None = None
	pais: str = "Espana"
	metodo_pago: str = "tarjeta"


class OrderAddressResponse(BaseModel):
	direccion: str
	ciudad: str
	codigo_postal: str | None = None
	pais: str
	principal: bool = False


class OrderItemDetailResponse(BaseModel):
	producto_id: int
	producto_nombre: str
	cantidad: int
	precio_unitario: float
	subtotal: float


class OrderItemResponse(BaseModel):
	producto_id: int
	cantidad: int
	precio_unitario: float
	subtotal: float


class OrderResponse(BaseModel):
	id: int
	usuario_id: int
	direccion_entrega_id: int
	estado: str
	subtotal: float
	impuestos: float
	costo_envio: float
	total: float
	metodo_pago: str
	fecha_creacion: datetime
	direccion_entrega: OrderAddressResponse | None = None
	items: List[OrderItemDetailResponse]

	class Config:
		from_attributes = True


class OrderListItemResponse(BaseModel):
	id: int
	usuario_id: int
	direccion_entrega_id: int
	estado: str
	total: float
	fecha_creacion: datetime
	items_total: int

	class Config:
		from_attributes = True


class OrderListResponse(BaseModel):
	items: List[OrderListItemResponse]
	total: int
	pagina: int
	tamano: int
