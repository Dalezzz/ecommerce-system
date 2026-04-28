from typing import Optional

from sqlalchemy.orm import Session, joinedload

from ..db.models import Carrito, Direccion, ItemOrden, Orden
from ..utils.exceptions import NotFoundError, ValidationError
from .cart_service import agregar_item, obtener_carrito_usuario, serializar_carrito


TAX_RATE = 0.16
SHIPPING_COST = 8.0
STOCK_MINIMO = 5
STOCK_CRITICO = 3


def _obtener_direccion(db: Session, usuario_id: int, direccion_entrega_id: int):
	direccion = (
		db.query(Direccion)
		.filter(Direccion.id == direccion_entrega_id, Direccion.usuario_id == usuario_id)
		.first()
	)
	if not direccion:
		raise ValidationError("La direccion de entrega no existe o no pertenece al usuario")
	return direccion


def _crear_direccion(db: Session, usuario_id: int, direccion: str, ciudad: str, codigo_postal: str | None, pais: str):
	direccion_obj = Direccion(
		usuario_id=usuario_id,
		direccion=direccion,
		ciudad=ciudad,
		codigo_postal=codigo_postal,
		pais=pais or "Espana",
		principal=False,
	)
	db.add(direccion_obj)
	db.flush()
	return direccion_obj


def _serializar_direccion(direccion: Direccion):
	return {
		"direccion": direccion.direccion,
		"ciudad": direccion.ciudad,
		"codigo_postal": direccion.codigo_postal,
		"pais": direccion.pais,
		"principal": bool(direccion.principal),
	}


def _serializar_orden(orden: Orden):
	direccion = _serializar_direccion(orden.direccion_entrega) if getattr(orden, "direccion_entrega", None) else None
	items = []
	for item in orden.items:
		items.append(
			{
				"producto_id": item.producto_id,
				"producto_nombre": item.producto.nombre if item.producto else "Producto",
				"cantidad": item.cantidad,
				"precio_unitario": float(item.precio_unitario),
				"subtotal": float(item.subtotal),
			}
		)

	return {
		"id": orden.id,
		"usuario_id": orden.usuario_id,
		"direccion_entrega_id": orden.direccion_entrega_id,
		"estado": orden.estado,
		"subtotal": float(orden.subtotal or 0.0),
		"impuestos": float(orden.impuestos or 0.0),
		"costo_envio": float(orden.costo_envio or 0.0),
		"total": float(orden.total),
		"metodo_pago": orden.metodo_pago,
		"fecha_creacion": orden.fecha_creacion,
		"direccion_entrega": direccion,
		"items": items,
	}


def crear_orden_desde_carrito(db: Session, usuario_id: int, direccion_data, metodo_pago: str = "tarjeta"):
	carrito = db.query(Carrito).filter(Carrito.usuario_id == usuario_id).first()
	if not carrito or not carrito.items:
		raise ValidationError("El carrito esta vacio")

	direccion_obj = _crear_direccion(
		db,
		usuario_id,
		direccion_data.direccion,
		direccion_data.ciudad,
		direccion_data.codigo_postal,
		direccion_data.pais,
	)

	subtotal = 0.0
	for item in carrito.items:
		if not item.producto or not item.producto.activo:
			raise ValidationError("Hay productos no disponibles en el carrito")
		if item.producto.stock < item.cantidad:
			raise ValidationError(
				f"Stock insuficiente para el producto {item.producto.nombre}. Reduce la cantidad o elimina el item del carrito."
			)
		subtotal += float(item.cantidad * item.precio_unitario)

	impuestos = round(subtotal * TAX_RATE, 2)
	orden_total = round(subtotal + impuestos + SHIPPING_COST, 2)

	orden = Orden(
		usuario_id=usuario_id,
		direccion_entrega_id=direccion_obj.id,
		estado="pagado",
		total=orden_total,
		subtotal=round(subtotal, 2),
		impuestos=impuestos,
		costo_envio=SHIPPING_COST,
		metodo_pago=metodo_pago,
	)
	db.add(orden)
	db.flush()

	for item in carrito.items:
		subtotal_item = float(item.cantidad * item.precio_unitario)
		orden_item = ItemOrden(
			orden_id=orden.id,
			producto_id=item.producto_id,
			cantidad=item.cantidad,
			precio_unitario=item.precio_unitario,
			subtotal=subtotal_item,
		)
		item.producto.stock -= item.cantidad
		db.add(orden_item)

	for item in list(carrito.items):
		db.delete(item)

	db.commit()
	db.refresh(orden)
	orden = obtener_orden_por_id(db, orden.id)
	return _serializar_orden(orden)


def obtener_orden_por_id(db: Session, orden_id: int):
	orden = db.query(Orden).options(joinedload(Orden.items).joinedload(ItemOrden.producto)).filter(Orden.id == orden_id).first()
	if not orden:
		raise NotFoundError("Pedido no encontrado")
	return orden


def listar_ordenes(db: Session, usuario_id: Optional[int] = None, estado: Optional[str] = None, pagina: int = 1, tamano: int = 10, orden_desc: bool = True):
	query = db.query(Orden).options(joinedload(Orden.items).joinedload(ItemOrden.producto))
	if usuario_id is not None:
		query = query.filter(Orden.usuario_id == usuario_id)
	if estado and estado.lower() != "todos":
		query = query.filter(Orden.estado == estado)

	total = query.count()
	query = query.order_by(Orden.fecha_creacion.desc() if orden_desc else Orden.fecha_creacion.asc())
	ordenes = query.offset((pagina - 1) * tamano).limit(tamano).all()

	items = []
	for orden in ordenes:
		items.append(
			{
				"id": orden.id,
				"usuario_id": orden.usuario_id,
				"direccion_entrega_id": orden.direccion_entrega_id,
				"estado": orden.estado,
				"total": float(orden.total),
				"fecha_creacion": orden.fecha_creacion,
				"items_total": len(orden.items),
			}
		)

	return {
		"items": items,
		"total": total,
		"pagina": pagina,
		"tamano": tamano,
	}


def detallar_orden(db: Session, orden: Orden):
	return _serializar_orden(orden)


def reordenar_pedido(db: Session, usuario_id: int, orden_id: int):
	orden = obtener_orden_por_id(db, orden_id)
	if orden.usuario_id != usuario_id:
		raise ValidationError("No puedes reordenar un pedido que no te pertenece")

	for item in orden.items:
		agregar_item(db, usuario_id, item.producto_id, item.cantidad)

	carrito = obtener_carrito_usuario(db, usuario_id)
	return serializar_carrito(carrito)


def cancelar_orden(db: Session, usuario_id: int, orden_id: int, es_admin: bool = False):
	orden = obtener_orden_por_id(db, orden_id)
	if not es_admin and orden.usuario_id != usuario_id:
		raise ValidationError("No puedes cancelar un pedido que no te pertenece")
	if orden.estado in {"enviada", "entregada", "cancelada"}:
		raise ValidationError("El pedido ya no puede cancelarse")

	for item in orden.items:
		if item.producto:
			item.producto.stock += item.cantidad

	orden.estado = "cancelada"
	db.commit()
	db.refresh(orden)
	return detallar_orden(db, orden)
