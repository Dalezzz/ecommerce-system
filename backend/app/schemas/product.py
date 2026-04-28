from typing import Optional

from pydantic import BaseModel, Field


class ProductBase(BaseModel):
	sku: str
	nombre: str
	descripcion: Optional[str] = None
	precio: float = Field(gt=0)
	stock: int = Field(ge=0)
	categoria_id: int
	imagen_url: Optional[str] = None


class ProductCreate(ProductBase):
	pass


class ProductUpdate(BaseModel):
	nombre: Optional[str] = None
	descripcion: Optional[str] = None
	precio: Optional[float] = Field(default=None, gt=0)
	stock: Optional[int] = Field(default=None, ge=0)
	categoria_id: Optional[int] = None
	imagen_url: Optional[str] = None
	activo: Optional[bool] = None


class CategoryResponse(BaseModel):
	id: int
	nombre: str
	descripcion: Optional[str] = None

	class Config:
		from_attributes = True


class ProductResponse(ProductBase):
	id: int
	activo: bool

	class Config:
		from_attributes = True
