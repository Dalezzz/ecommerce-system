import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

import { AuthTokenService } from '../../../../core/services/auth-token.service';
import { CartStateService } from '../../../../core/services/cart-state.service';
import { NotificationService } from '../../../../core/services/notification.service';
import { OrderDetail, OrderSummary } from '../../../../core/models/order.model';
import { OrdersApiService } from '../../../../core/services/orders-api.service';

@Component({
  selector: 'app-orders-page',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './orders-page.component.html',
  styleUrl: './orders-page.component.scss',
})
export class OrdersPageComponent {
  orders: OrderSummary[] = [];
  loading = true;
  errorMessage: string | null = null;
  selectedOrder: OrderDetail | null = null;
  statusFilter = 'todos';
  sortOrder: 'desc' | 'asc' = 'desc';
  page = 1;
  pageSize = 6;
  total = 0;
  isAdmin = false;

  constructor(
    private readonly ordersApi: OrdersApiService,
    private readonly authToken: AuthTokenService,
    private readonly notifier: NotificationService,
    private readonly cartState: CartStateService
  ) {}

  ngOnInit(): void {
    this.isAdmin = this.authToken.getRole() === 'admin';
    this.loadOrders();
  }

  loadOrders(resetPage = false): void {
    if (resetPage) {
      this.page = 1;
    }

    this.loading = true;
    this.errorMessage = null;

    const request = this.isAdmin
      ? this.ordersApi.listAll({
          estado: this.statusFilter,
          pagina: this.page,
          tamano: this.pageSize,
          orden: this.sortOrder,
        })
      : this.ordersApi.listMine({
          estado: this.statusFilter,
          pagina: this.page,
          tamano: this.pageSize,
          orden: this.sortOrder,
        });

    request.subscribe({
      next: (response) => {
        this.orders = response.items;
        this.total = response.total;
        this.loading = false;
      },
      error: (error) => {
        this.errorMessage = error?.error?.detail ?? 'No fue posible cargar tus pedidos';
        this.loading = false;
      },
    });
  }

  selectOrder(orderId: number): void {
    this.ordersApi.getById(orderId).subscribe({
      next: (order) => {
        this.selectedOrder = order;
      },
      error: (error) => {
        this.notifier.warn(error?.error?.detail ?? 'No fue posible cargar el detalle del pedido');
      },
    });
  }

  reorder(orderId: number): void {
    this.ordersApi.reorder(orderId).subscribe({
      next: (cart) => {
        this.cartState.syncFromCart(cart);
        this.notifier.info('Productos del pedido agregados al carrito');
      },
      error: (error) => {
        this.notifier.warn(error?.error?.detail ?? 'No fue posible reordenar el pedido');
      },
    });
  }

  cancelSelectedOrder(): void {
    if (!this.selectedOrder) {
      return;
    }

    this.ordersApi.cancel(this.selectedOrder.id).subscribe({
      next: (order) => {
        this.selectedOrder = order;
        this.notifier.info('Pedido cancelado correctamente');
        this.loadOrders();
      },
      error: (error) => {
        this.notifier.warn(error?.error?.detail ?? 'No fue posible cancelar el pedido');
      },
    });
  }

  setStatusFilter(value: string): void {
    this.statusFilter = value;
    this.loadOrders(true);
  }

  setSortOrder(value: string): void {
    this.sortOrder = value === 'asc' ? 'asc' : 'desc';
    this.loadOrders(true);
  }

  previousPage(): void {
    if (this.page > 1) {
      this.page -= 1;
      this.loadOrders();
    }
  }

  nextPage(): void {
    if (this.page * this.pageSize < this.total) {
      this.page += 1;
      this.loadOrders();
    }
  }

  canCancel(order: OrderDetail | null): boolean {
    return !!order && !['cancelada', 'enviada', 'entregada'].includes(order.estado);
  }
}
