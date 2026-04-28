import { Routes } from '@angular/router';
import { authGuard } from '../../core/guards/auth.guard';

export const CART_ROUTES: Routes = [
  {
    path: '',
    loadComponent: () => import('./pages/cart-page/cart-page.component').then((m) => m.CartPageComponent),
  },
  {
    path: 'checkout',
    canActivate: [authGuard],
    loadComponent: () =>
      import('./pages/checkout-page/checkout-page.component').then((m) => m.CheckoutPageComponent),
  },
];