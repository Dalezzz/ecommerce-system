import { Injectable, signal } from '@angular/core';

import { Cart } from '../models/cart.model';
import { Product } from '../models/product.model';

export interface GuestCartItem {
  producto_id: number;
  nombre: string;
  cantidad: number;
  precio_unitario: number;
}

const GUEST_CART_KEY = 'storefront_guest_cart';

@Injectable({ providedIn: 'root' })
export class CartStateService {
  private readonly countState = signal(0);
  readonly count = this.countState.asReadonly();

  syncFromCart(cart: Cart): void {
    const totalItems = cart.items.reduce((sum, item) => sum + item.cantidad, 0);
    this.countState.set(totalItems);
  }

  syncGuestCount(): void {
    this.countState.set(this.readGuestItems().reduce((sum, item) => sum + item.cantidad, 0));
  }

  getGuestItems(): GuestCartItem[] {
    return this.readGuestItems();
  }

  addGuestItem(product: Product, cantidad = 1): void {
    const items = this.readGuestItems();
    const item = items.find((entry) => entry.producto_id === product.id);

    if (item) {
      item.cantidad += cantidad;
    } else {
      items.push({
        producto_id: product.id,
        nombre: product.nombre,
        cantidad,
        precio_unitario: product.precio,
      });
    }

    localStorage.setItem(GUEST_CART_KEY, JSON.stringify(items));
    this.syncGuestCount();
  }

  removeGuestItem(productoId: number): void {
    const items = this.readGuestItems().filter((item) => item.producto_id !== productoId);
    localStorage.setItem(GUEST_CART_KEY, JSON.stringify(items));
    this.syncGuestCount();
  }

  clearGuestCart(): void {
    localStorage.removeItem(GUEST_CART_KEY);
    this.syncGuestCount();
  }

  clear(): void {
    this.countState.set(0);
  }

  private readGuestItems(): GuestCartItem[] {
    try {
      const raw = localStorage.getItem(GUEST_CART_KEY);
      if (!raw) {
        return [];
      }

      const parsed = JSON.parse(raw) as GuestCartItem[];
      return Array.isArray(parsed) ? parsed : [];
    } catch {
      return [];
    }
  }
}