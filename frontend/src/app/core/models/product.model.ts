export interface Product {
  id: number;
  sku: string;
  nombre: string;
  descripcion: string | null;
  precio: number;
  stock: number;
  categoria_id: number;
  imagen_url: string | null;
  activo: boolean;
}

export interface Category {
  id: number;
  nombre: string;
  descripcion: string | null;
}
