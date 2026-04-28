import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';

import { Cart } from '../../../../core/models/cart.model';
import { AuthTokenService } from '../../../../core/services/auth-token.service';
import { CartApiService } from '../../../../core/services/cart-api.service';
import { CartStateService, GuestCartItem } from '../../../../core/services/cart-state.service';
import { NotificationService } from '../../../../core/services/notification.service';

type CartLineItem = GuestCartItem & { subtotal: number };

@Component({
  selector: 'app-cart-page',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './cart-page.component.html',
  styleUrl: './cart-page.component.scss',
})
export class CartPageComponent {
  loading = true;
  errorMessage: string | null = null;
  isAuthenticated = false;
  items: CartLineItem[] = [];
  total = 0;

  constructor(
    private readonly authToken: AuthTokenService,
    private readonly cartApi: CartApiService,
    private readonly cartState: CartStateService,
    private readonly notifier: NotificationService
  ) {}

  ngOnInit(): void {
    this.isAuthenticated = this.authToken.isAuthenticated();
    this.loadCart();
  }

  loadCart(): void {
    this.loading = true;
    this.errorMessage = null;

    if (!this.isAuthenticated) {
      this.loadGuestCart();
      return;
    }

    this.cartApi.getMyCart().subscribe({
      next: (cart) => this.applyRemoteCart(cart),
      error: (error) => {
        this.errorMessage = error?.error?.detail ?? 'No fue posible cargar tu carrito';
        this.loading = false;
      },
    });
  }

  removeItem(productoId: number): void {
    if (!this.isAuthenticated) {
      this.cartState.removeGuestItem(productoId);
      this.loadGuestCart();
      this.notifier.info('Producto eliminado del carrito local');
      return;
    }

    this.cartApi.removeItem(productoId).subscribe({
      next: (cart) => {
        this.applyRemoteCart(cart);
        this.notifier.info('Producto eliminado del carrito');
      },
      error: (error) => {
        this.notifier.warn(error?.error?.detail ?? 'No fue posible eliminar el producto');
      },
    });
  }

  clearCart(): void {
    if (!this.isAuthenticated) {
      this.cartState.clearGuestCart();
      this.loadGuestCart();
      this.notifier.info('Carrito local vaciado');
      return;
    }

    this.cartApi.clearCart().subscribe({
      next: (cart) => {
        this.applyRemoteCart(cart);
        this.notifier.info('Carrito vaciado');
      },
      error: (error) => {
        this.notifier.warn(error?.error?.detail ?? 'No fue posible vaciar el carrito');
      },
    });
  }

  private loadGuestCart(): void {
    const guestItems = this.cartState.getGuestItems();
    this.items = guestItems.map((item) => ({
      ...item,
      subtotal: item.cantidad * item.precio_unitario,
    }));
    this.total = this.items.reduce((sum, item) => sum + item.subtotal, 0);
    this.loading = false;
    this.cartState.syncGuestCount();
  }

  private applyRemoteCart(cart: Cart): void {
    this.items = cart.items.map((item) => ({
      producto_id: item.producto_id,
      nombre: item.nombre,
      cantidad: item.cantidad,
      precio_unitario: item.precio_unitario,
      subtotal: item.subtotal,
    }));
    this.total = cart.total;
    this.loading = false;
    this.cartState.syncFromCart(cart);
  }
}