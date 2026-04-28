from sqlalchemy import func
from sqlalchemy.orm import Session

from ..db.models import Categoria, ItemOrden, Orden, Producto

STOCK_MINIMO = 5
STOCK_CRITICO = 3


def resumen_ventas(db: Session):
	total_ordenes = db.query(func.count(Orden.id)).scalar() or 0
	ingresos_totales = db.query(func.coalesce(func.sum(Orden.total), 0.0)).scalar() or 0.0
	return {
		"total_ordenes": int(total_ordenes),
		"ingresos_totales": float(ingresos_totales),
	}


def top_productos(db: Session, limite: int = 5):
	rows = (
		db.query(
			ItemOrden.producto_id,
			func.sum(ItemOrden.cantidad).label("cantidad_total"),
			func.sum(ItemOrden.subtotal).label("ingreso_total"),
		)
		.group_by(ItemOrden.producto_id)
		.order_by(func.sum(ItemOrden.cantidad).desc())
		.limit(limite)
		.all()
	)

	return [
		{
			"producto_id": row.producto_id,
			"cantidad_total": int(row.cantidad_total or 0),
			"ingreso_total": float(row.ingreso_total or 0.0),
		}
		for row in rows
	]


def inventario_alertas(db: Session, categoria_id: int | None = None, solo_criticos: bool = False):
	query = db.query(Producto, Categoria.nombre.label("categoria_nombre")).outerjoin(Categoria, Producto.categoria_id == Categoria.id)
	if categoria_id is not None:
		query = query.filter(Producto.categoria_id == categoria_id)

	rows = query.order_by(Producto.stock.asc(), Producto.nombre.asc()).all()
	resultado = []
	for producto, categoria_nombre in rows:
		if producto.stock == 0:
			estado = "critical"
			color = "red"
		elif producto.stock < STOCK_CRITICO:
			estado = "critical"
			color = "red"
		elif producto.stock < STOCK_MINIMO:
			estado = "warning"
			color = "yellow"
		else:
			estado = "ok"
			color = "green"

		if solo_criticos and estado == "ok":
			continue

		resultado.append(
			{
				"producto_id": producto.id,
				"sku": producto.sku,
				"nombre": producto.nombre,
				"categoria": categoria_nombre,
				"stock_actual": int(producto.stock),
				"stock_minimo": STOCK_MINIMO,
				"umbral_critico": STOCK_CRITICO,
				"estado": estado,
				"color": color,
			}
		)

	return resultado
