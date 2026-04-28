from sqlalchemy.orm import Session

from ..db.models import Producto, Categoria
from ..schemas.product import ProductCreate, ProductUpdate
from ..utils.exceptions import ConflictError


def listar_categorias(db: Session):
	return db.query(Categoria).all()


def listar_productos(db: Session, solo_activos: bool = True, search: str = None, category_id: int = None):
	query = db.query(Producto)
	if solo_activos:
		query = query.filter(Producto.activo.is_(True))
	if search:
		query = query.filter(Producto.nombre.ilike(f"%{search}%"))
	if category_id:
		query = query.filter(Producto.categoria_id == category_id)
	return query.all()


def obtener_producto(db: Session, producto_id: int):
	return db.query(Producto).filter(Producto.id == producto_id).first()


def crear_producto(db: Session, data: ProductCreate):
	if db.query(Producto).filter(Producto.sku == data.sku).first():
		raise ConflictError("Ya existe un producto con ese SKU")
	producto = Producto(**data.model_dump())
	db.add(producto)
	db.commit()
	db.refresh(producto)
	return producto


def actualizar_producto(db: Session, producto: Producto, data: ProductUpdate):
	update_data = data.model_dump(exclude_unset=True)

	for field, value in update_data.items():
		setattr(producto, field, value)

	if db.query(Producto).filter(Producto.id != producto.id, Producto.sku == producto.sku).first():
		raise ConflictError("Ya existe un producto con ese SKU")

	db.commit()
	db.refresh(producto)
	return producto


def desactivar_producto(db: Session, producto: Producto):
	producto.activo = False
	db.commit()
	db.refresh(producto)
	return producto
