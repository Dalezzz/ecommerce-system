import { Injectable } from '@angular/core';

import { Observable } from 'rxjs';

import { Cart } from '../models/cart.model';
import { OrderCheckoutRequest, OrderDetail, OrderListResponse } from '../models/order.model';
import { ApiService } from './api.service';

export interface OrderQueryParams {
  estado?: string;
  pagina?: number;
  tamano?: number;
  orden?: 'asc' | 'desc';
}

@Injectable({ providedIn: 'root' })
export class OrdersApiService {
  constructor(private readonly api: ApiService) {}

  listMine(params: OrderQueryParams = {}): Observable<OrderListResponse> {
    return this.api.get<OrderListResponse>('/orders/mine', params as Record<string, string | number | boolean | null | undefined>);
  }

  listAll(params: OrderQueryParams = {}): Observable<OrderListResponse> {
    return this.api.get<OrderListResponse>('/orders', params as Record<string, string | number | boolean | null | undefined>);
  }

  getById(orderId: number): Observable<OrderDetail> {
    return this.api.get<OrderDetail>(`/orders/${orderId}`);
  }

  reorder(orderId: number): Observable<Cart> {
    return this.api.post<Cart>(`/orders/${orderId}/reorder`, {});
  }

  cancel(orderId: number): Observable<OrderDetail> {
    return this.api.post<OrderDetail>(`/orders/${orderId}/cancel`, {});
  }

  checkout(payload: OrderCheckoutRequest): Observable<OrderDetail> {
    return this.api.post<OrderDetail>('/orders/checkout', payload);
  }
}
