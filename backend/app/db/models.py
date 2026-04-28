from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
from .database import Base
import datetime
import enum

class RolUsuario(str, enum.Enum):
    admin = "admin"
    cliente = "cliente"

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    nombre = Column(String, nullable=False)
    rol = Column(Enum(RolUsuario), default=RolUsuario.cliente)
    fecha_registro = Column(DateTime, default=datetime.datetime.utcnow)
    carrito = relationship("Carrito", uselist=False, back_populates="usuario")
    ordenes = relationship("Orden", back_populates="usuario")

class Categoria(Base):
    __tablename__ = "categorias"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)
    descripcion = Column(String)
    productos = relationship("Producto", back_populates="categoria")

class Producto(Base):
    __tablename__ = "productos"
    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String, unique=True, index=True, nullable=False)
    nombre = Column(String, nullable=False)
    descripcion = Column(String)
    precio = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    categoria_id = Column(Integer, ForeignKey("categorias.id"))
    imagen_url = Column(String)
    activo = Column(Boolean, default=True)
    categoria = relationship("Categoria", back_populates="productos")

class Carrito(Base):
    __tablename__ = "carritos"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), unique=True)
    usuario = relationship("Usuario", back_populates="carrito")
    items = relationship("ItemCarrito", back_populates="carrito", cascade="all, delete-orphan")

class ItemCarrito(Base):
    __tablename__ = "items_carrito"
    id = Column(Integer, primary_key=True, index=True)
    carrito_id = Column(Integer, ForeignKey("carritos.id"))
    producto_id = Column(Integer, ForeignKey("productos.id"))
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False)
    producto = relationship("Producto")
    carrito = relationship("Carrito", back_populates="items")

class Direccion(Base):
    __tablename__ = "direcciones"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    direccion = Column(String, nullable=False)
    ciudad = Column(String, nullable=False)
    codigo_postal = Column(String)
    pais = Column(String, default="Espana")
    principal = Column(Boolean, default=False)

class Orden(Base):
    __tablename__ = "ordenes"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    direccion_entrega_id = Column(Integer, ForeignKey("direcciones.id"))
    estado = Column(String, default="pendiente")  # pendiente, confirmada, enviada, entregada, cancelada
    total = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False, default=0.0)
    impuestos = Column(Float, nullable=False, default=0.0)
    costo_envio = Column(Float, nullable=False, default=0.0)
    metodo_pago = Column(String, nullable=False, default="tarjeta")
    fecha_creacion = Column(DateTime, default=datetime.datetime.utcnow)
    fecha_actualizacion = Column(DateTime, onupdate=datetime.datetime.utcnow)
    items = relationship("ItemOrden", back_populates="orden")
    usuario = relationship("Usuario", back_populates="ordenes")
    direccion_entrega = relationship("Direccion")

class ItemOrden(Base):
    __tablename__ = "items_orden"
    id = Column(Integer, primary_key=True, index=True)
    orden_id = Column(Integer, ForeignKey("ordenes.id"))
    producto_id = Column(Integer, ForeignKey("productos.id"))
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)
    orden = relationship("Orden", back_populates="items")
    producto = relationship("Producto")