from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db.database import get_db
from ..schemas.product import ProductCreate, ProductResponse, ProductUpdate, CategoryResponse
from ..services.product_service import (
	actualizar_producto,
	crear_producto,
	desactivar_producto,
	listar_productos,
	obtener_producto,
	listar_categorias,
)
from ..utils.security import require_admin

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/categories", response_model=list[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
	return listar_categorias(db)


@router.get("/", response_model=list[ProductResponse])
def get_products(
	search: str | None = None,
	category_id: int | None = None,
	db: Session = Depends(get_db)
):
	return listar_productos(db, search=search, category_id=category_id)


@router.get("/{producto_id}", response_model=ProductResponse)
def get_product(producto_id: int, db: Session = Depends(get_db)):
	producto = obtener_producto(db, producto_id)
	if not producto or not producto.activo:
		raise HTTPException(status_code=404, detail="Producto no encontrado")
	return producto


@router.post("/", response_model=ProductResponse, status_code=201)
def create_product(
	payload: ProductCreate,
	db: Session = Depends(get_db),
	_=Depends(require_admin),
):
	return crear_producto(db, payload)


@router.put("/{producto_id}", response_model=ProductResponse)
def update_product(
	producto_id: int,
	payload: ProductUpdate,
	db: Session = Depends(get_db),
	_=Depends(require_admin),
):
	producto = obtener_producto(db, producto_id)
	if not producto:
		raise HTTPException(status_code=404, detail="Producto no encontrado")
	return actualizar_producto(db, producto, payload)


@router.delete("/{producto_id}", response_model=ProductResponse)
def delete_product(
	producto_id: int,
	db: Session = Depends(get_db),
	_=Depends(require_admin),
):
	producto = obtener_producto(db, producto_id)
	if not producto:
		raise HTTPException(status_code=404, detail="Producto no encontrado")
	return desactivar_producto(db, producto)
