export interface CartItem {
  producto_id: number;
  nombre: string;
  cantidad: number;
  precio_unitario: number;
  subtotal: number;
}

export interface Cart {
  id: number;
  usuario_id: number;
  items: CartItem[];
  total: number;
}
