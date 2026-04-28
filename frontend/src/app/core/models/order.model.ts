export interface OrderItem {
  producto_id: number;
  cantidad: number;
  precio_unitario: number;
  subtotal: number;
}

export interface OrderCheckoutRequest {
  direccion: string;
  ciudad: string;
  codigo_postal?: string | null;
  pais?: string;
  metodo_pago: string;
}

export interface OrderAddress {
  direccion: string;
  ciudad: string;
  codigo_postal: string | null;
  pais: string;
  principal: boolean;
}

export interface OrderItemDetail {
  producto_id: number;
  producto_nombre: string;
  cantidad: number;
  precio_unitario: number;
  subtotal: number;
}

export interface OrderSummary {
  id: number;
  usuario_id: number;
  direccion_entrega_id: number;
  estado: string;
  total: number;
  fecha_creacion: string;
  items_total: number;
}

export interface OrderDetail extends OrderSummary {
  subtotal: number;
  impuestos: number;
  costo_envio: number;
  metodo_pago: string;
  direccion_entrega: OrderAddress | null;
  items: OrderItemDetail[];
}

export interface OrderListResponse {
  items: OrderSummary[];
  total: number;
  pagina: number;
  tamano: number;
}
