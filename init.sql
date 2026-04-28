CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    email VARCHAR NOT NULL UNIQUE,
    password_hash VARCHAR NOT NULL,
    nombre VARCHAR NOT NULL,
    rol VARCHAR NOT NULL DEFAULT 'cliente',
    fecha_registro TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS categorias (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR NOT NULL UNIQUE,
    descripcion VARCHAR
);

CREATE TABLE IF NOT EXISTS productos (
    id SERIAL PRIMARY KEY,
    sku VARCHAR NOT NULL UNIQUE,
    nombre VARCHAR NOT NULL,
    descripcion VARCHAR,
    precio DOUBLE PRECISION NOT NULL,
    stock INTEGER NOT NULL DEFAULT 0,
    categoria_id INTEGER REFERENCES categorias(id),
    imagen_url VARCHAR,
    activo BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS carritos (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER UNIQUE REFERENCES usuarios(id)
);

CREATE TABLE IF NOT EXISTS items_carrito (
    id SERIAL PRIMARY KEY,
    carrito_id INTEGER REFERENCES carritos(id),
    producto_id INTEGER REFERENCES productos(id),
    cantidad INTEGER NOT NULL,
    precio_unitario DOUBLE PRECISION NOT NULL
);

CREATE TABLE IF NOT EXISTS direcciones (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(id),
    direccion VARCHAR NOT NULL,
    ciudad VARCHAR NOT NULL,
    codigo_postal VARCHAR,
    pais VARCHAR DEFAULT 'Espana',
    principal BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS ordenes (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(id),
    direccion_entrega_id INTEGER REFERENCES direcciones(id),
    estado VARCHAR DEFAULT 'pendiente',
    total DOUBLE PRECISION NOT NULL,
    subtotal DOUBLE PRECISION NOT NULL DEFAULT 0,
    impuestos DOUBLE PRECISION NOT NULL DEFAULT 0,
    costo_envio DOUBLE PRECISION NOT NULL DEFAULT 0,
    metodo_pago VARCHAR NOT NULL DEFAULT 'tarjeta',
    fecha_creacion TIMESTAMP NOT NULL DEFAULT NOW(),
    fecha_actualizacion TIMESTAMP
);

CREATE TABLE IF NOT EXISTS items_orden (
    id SERIAL PRIMARY KEY,
    orden_id INTEGER REFERENCES ordenes(id),
    producto_id INTEGER REFERENCES productos(id),
    cantidad INTEGER NOT NULL,
    precio_unitario DOUBLE PRECISION NOT NULL,
    subtotal DOUBLE PRECISION NOT NULL
);

INSERT INTO categorias (nombre, descripcion) VALUES
    ('Electronica', 'Dispositivos y accesorios tecnologicos'),
    ('Hogar', 'Articulos para casa y oficina'),
    ('Moda', 'Ropa y accesorios')
ON CONFLICT (nombre) DO NOTHING;

INSERT INTO productos (sku, nombre, descripcion, precio, stock, categoria_id, imagen_url, activo) VALUES
    ('SKU001', 'Auriculares Bluetooth', 'Cancelacion de ruido', 79.99, 120, 1, 'https://picsum.photos/seed/prod1/640/480', TRUE),
    ('SKU002', 'Teclado Mecanico', 'Switches lineales, formato TKL', 59.50, 80, 1, 'https://picsum.photos/seed/prod2/640/480', TRUE),
    ('SKU003', 'Lampara Escritorio', 'Luz LED regulable', 25.00, 200, 2, 'https://picsum.photos/seed/prod3/640/480', TRUE),
    ('SKU004', 'Silla Ergonomica', 'Soporte lumbar y ajuste de altura', 229.90, 35, 2, 'https://picsum.photos/seed/prod4/640/480', TRUE),
    ('SKU005', 'Chaqueta Impermeable', 'Ligera, resistente al agua', 89.00, 60, 3, 'https://picsum.photos/seed/prod5/640/480', TRUE)
ON CONFLICT (sku) DO NOTHING;

-- Los usuarios, carritos, direcciones y ordenes se crean desde la API.