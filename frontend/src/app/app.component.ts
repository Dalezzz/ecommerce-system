import { Component } from '@angular/core';
import { Router, RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { NgIf } from '@angular/common';

import { AuthTokenService } from './core/services/auth-token.service';
import { CartStateService } from './core/services/cart-state.service';
import { NotificationService } from './core/services/notification.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [NgIf, RouterOutlet, RouterLink, RouterLinkActive],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  readonly title = 'Storefront';
  readonly cartCount = this.cartState.count;
  readonly notification = this.notifications.current;

  constructor(
    private readonly tokenService: AuthTokenService,
    private readonly cartState: CartStateService,
    private readonly notifications: NotificationService,
    private readonly router: Router
  ) {}

  logout(): void {
    this.tokenService.clearToken();
    this.cartState.clear();
    this.router.navigate(['/auth/login']);
  }

  get isAuthenticated(): boolean {
    return this.tokenService.isAuthenticated();
  }

  get isAdmin(): boolean {
    return this.tokenService.getRole() === 'admin';
  }

  get showCartLink(): boolean {
    return true;
  }
}
