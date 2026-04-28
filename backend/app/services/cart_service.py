from sqlalchemy.orm import Session
from ..db.models import Carrito, ItemCarrito, Producto
from ..utils.exceptions import ValidationError

def obtener_carrito_usuario(db: Session, usuario_id: int):
    carrito = db.query(Carrito).filter(Carrito.usuario_id == usuario_id).first()
    if not carrito:
        carrito = Carrito(usuario_id=usuario_id)
        db.add(carrito)
        db.commit()
        db.refresh(carrito)
    return carrito

def agregar_item(db: Session, usuario_id: int, producto_id: int, cantidad: int):
    producto = db.query(Producto).filter(Producto.id == producto_id, Producto.activo.is_(True)).first()
    if not producto:
        raise ValidationError("Producto no disponible")
    carrito = obtener_carrito_usuario(db, usuario_id)
    item = db.query(ItemCarrito).filter(
        ItemCarrito.carrito_id == carrito.id,
        ItemCarrito.producto_id == producto_id
    ).first()
    cantidad_existente = item.cantidad if item else 0
    if producto.stock < cantidad_existente + cantidad:
        raise ValidationError("Stock insuficiente para la cantidad solicitada")
    if item:
        item.cantidad += cantidad
        item.precio_unitario = producto.precio
    else:
        item = ItemCarrito(
            carrito_id=carrito.id,
            producto_id=producto_id,
            cantidad=cantidad,
            precio_unitario=producto.precio
        )
        db.add(item)
    db.commit()
    db.refresh(carrito)
    return carrito


def quitar_item(db: Session, usuario_id: int, producto_id: int):
    carrito = obtener_carrito_usuario(db, usuario_id)
    item = db.query(ItemCarrito).filter(
        ItemCarrito.carrito_id == carrito.id,
        ItemCarrito.producto_id == producto_id,
    ).first()
    if not item:
        raise ValidationError("El producto no existe en el carrito")
    db.delete(item)
    db.commit()
    db.refresh(carrito)
    return carrito


def limpiar_carrito(db: Session, usuario_id: int):
    carrito = obtener_carrito_usuario(db, usuario_id)
    db.query(ItemCarrito).filter(ItemCarrito.carrito_id == carrito.id).delete()
    db.commit()
    db.refresh(carrito)
    return carrito


def serializar_carrito(carrito: Carrito):
    items = []
    total = 0.0
    for item in carrito.items:
        subtotal = float(item.cantidad * item.precio_unitario)
        total += subtotal
        items.append(
            {
                "producto_id": item.producto_id,
                "nombre": item.producto.nombre if item.producto else "Producto",
                "cantidad": item.cantidad,
                "precio_unitario": float(item.precio_unitario),
                "subtotal": subtotal,
            }
        )

    return {
        "id": carrito.id,
        "usuario_id": carrito.usuario_id,
        "items": items,
        "total": total,
    }