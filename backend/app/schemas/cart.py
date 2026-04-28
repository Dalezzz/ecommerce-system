from typing import List

from pydantic import BaseModel, Field


class CartItemAdd(BaseModel):
	producto_id: int
	cantidad: int = Field(gt=0)


class CartItemResponse(BaseModel):
	producto_id: int
	nombre: str
	cantidad: int
	precio_unitario: float
	subtotal: float


class CartResponse(BaseModel):
	id: int
	usuario_id: int
	items: List[CartItemResponse]
	total: float
