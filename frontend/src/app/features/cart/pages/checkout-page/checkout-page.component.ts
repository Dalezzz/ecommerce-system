import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';

import { finalize } from 'rxjs';

import { Cart } from '../../../../core/models/cart.model';
import { OrderDetail } from '../../../../core/models/order.model';
import { CartApiService } from '../../../../core/services/cart-api.service';
import { CartStateService } from '../../../../core/services/cart-state.service';
import { NotificationService } from '../../../../core/services/notification.service';
import { OrdersApiService } from '../../../../core/services/orders-api.service';
import { PaymentGatewaySandboxService } from '../../../../core/services/payment-gateway-sandbox.service';

@Component({
  selector: 'app-checkout-page',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  templateUrl: './checkout-page.component.html',
  styleUrl: './checkout-page.component.scss',
})
export class CheckoutPageComponent {
  loading = true;
  processing = false;
  errorMessage: string | null = null;
  successOrder: OrderDetail | null = null;
  cart: Cart | null = null;

  readonly form = this.fb.nonNullable.group({
    direccion: ['', [Validators.required, Validators.minLength(5)]],
    ciudad: ['', [Validators.required, Validators.minLength(2)]],
    codigo_postal: ['', [Validators.required, Validators.minLength(3)]],
    pais: ['Espana', [Validators.required]],
    metodo_pago: ['stripe', [Validators.required]],
    cardHolder: ['', [Validators.required, Validators.minLength(3)]],
    cardNumber: ['', [Validators.required, Validators.minLength(12), Validators.maxLength(19)]],
    expiry: ['', [Validators.required]],
    cvv: ['', [Validators.required, Validators.minLength(3), Validators.maxLength(4)]],
  });

  constructor(
    private readonly fb: FormBuilder,
    private readonly cartApi: CartApiService,
    private readonly ordersApi: OrdersApiService,
    private readonly gateway: PaymentGatewaySandboxService,
    private readonly cartState: CartStateService,
    private readonly notifier: NotificationService,
    private readonly router: Router
  ) {}

  ngOnInit(): void {
    this.cartApi.getMyCart().subscribe({
      next: (cart) => {
        this.cart = cart;
        this.cartState.syncFromCart(cart);
        this.loading = false;
      },
      error: (error) => {
        this.errorMessage = error?.error?.detail ?? 'No fue posible cargar el carrito para pagar';
        this.loading = false;
      },
    });
  }

  submit(): void {
    if (this.form.invalid || !this.cart || this.cart.items.length === 0) {
      this.form.markAllAsTouched();
      return;
    }

    this.processing = true;
    this.errorMessage = null;
    this.successOrder = null;

    const formValue = this.form.getRawValue();
    const amount = this.cart.total;

    this.gateway
      .authorizePayment({
        cardHolder: formValue.cardHolder,
        cardNumber: formValue.cardNumber,
        expiry: formValue.expiry,
        cvv: formValue.cvv,
        amount,
        gateway: formValue.metodo_pago as 'stripe' | 'mercadopago' | 'paypal',
      })
      .pipe(finalize(() => (this.processing = false)))
      .subscribe({
        next: () => {
          this.ordersApi
            .checkout({
              direccion: formValue.direccion,
              ciudad: formValue.ciudad,
              codigo_postal: formValue.codigo_postal,
              pais: formValue.pais,
              metodo_pago: formValue.metodo_pago,
            })
            .subscribe({
              next: (order) => {
                this.successOrder = order;
                this.cartState.clear();
                this.cart = null;
                this.notifier.info('Pago aprobado y pedido creado correctamente');
                this.router.navigate(['/orders']);
              },
              error: (error) => {
                this.errorMessage = error?.error?.detail ?? 'El pago fue aprobado, pero no se pudo crear la orden';
              },
            });
        },
        error: (error) => {
          this.errorMessage = error?.message ?? 'La pasarela de pago rechazo la tarjeta';
          this.notifier.warn(this.errorMessage ?? 'La pasarela de pago rechazo la tarjeta');
        },
      });
  }
}