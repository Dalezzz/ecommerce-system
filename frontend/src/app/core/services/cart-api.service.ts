import { Injectable } from '@angular/core';

import { Observable } from 'rxjs';

import { Cart } from '../models/cart.model';
import { ApiService } from './api.service';

@Injectable({ providedIn: 'root' })
export class CartApiService {
  constructor(private readonly api: ApiService) {}

  addItem(productoId: number, cantidad = 1): Observable<Cart> {
    return this.api.post<Cart>('/cart/items', {
      producto_id: productoId,
      cantidad,
    });
  }

  getMyCart(): Observable<Cart> {
    return this.api.get<Cart>('/cart/');
  }

  removeItem(productoId: number): Observable<Cart> {
    return this.api.delete<Cart>(`/cart/items/${productoId}`);
  }

  clearCart(): Observable<Cart> {
    return this.api.delete<Cart>('/cart/');
  }
}
