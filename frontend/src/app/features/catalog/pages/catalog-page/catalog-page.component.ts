import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { Product, Category } from '../../../../core/models/product.model';
import { AuthTokenService } from '../../../../core/services/auth-token.service';
import { CartStateService } from '../../../../core/services/cart-state.service';
import { CartApiService } from '../../../../core/services/cart-api.service';
import { NotificationService } from '../../../../core/services/notification.service';
import { ProductsApiService } from '../../../../core/services/products-api.service';

@Component({
  selector: 'app-catalog-page',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './catalog-page.component.html',
  styleUrl: './catalog-page.component.scss',
})
export class CatalogPageComponent {
  products: Product[] = [];
  categories: Category[] = [];
  loading = true;
  errorMessage: string | null = null;
  addingProductId: number | null = null;
  
  // Search and filter
  searchTerm = '';
  selectedCategoryId: number | null = null;

  private authenticated = false;
  isAdmin = false;

  constructor(
    private readonly productsApi: ProductsApiService,
    private readonly cartApi: CartApiService,
    private readonly notifier: NotificationService,
    private readonly authToken: AuthTokenService,
    private readonly cartState: CartStateService
  ) {}

  ngOnInit(): void {
    this.authenticated = this.authToken.isAuthenticated();
    this.isAdmin = this.authToken.getRole() === 'admin';
    this.loadProducts();
    this.loadCategories();
  }

  loadProducts(): void {
    this.loading = true;
    this.productsApi.list(this.searchTerm, this.selectedCategoryId || undefined).subscribe({
      next: (products) => {
        this.products = products;
        this.loading = false;
        if (this.authenticated) {
          this.loadCartCount();
        } else {
          this.cartState.syncGuestCount();
        }
      },
      error: (error) => {
        this.errorMessage = error?.error?.detail ?? 'No fue posible cargar el catalogo';
        this.loading = false;
      },
    });
  }

  loadCategories(): void {
    this.productsApi.getCategories().subscribe({
      next: (categories) => {
        this.categories = categories;
      },
    });
  }

  onSearch(): void {
    this.loadProducts();
  }

  onCategoryChange(): void {
    this.loadProducts();
  }

  addToCart(product: Product): void {
    if (this.addingProductId !== null) {
      return;
    }

    this.addingProductId = product.id;

    if (!this.authenticated) {
      this.cartState.addGuestItem(product, 1);
      this.notifier.success(`Producto añadido al carrito local: ${product.nombre}`);
      this.addingProductId = null;
      return;
    }

    this.cartApi.addItem(product.id, 1).subscribe({
      next: () => {
        this.notifier.success(`Producto agregado al carrito: ${product.nombre}`);
        this.loadCartCount();
        this.addingProductId = null;
      },
      error: (error) => {
        const detail = error?.error?.detail ?? 'No se pudo agregar el producto al carrito';
        this.notifier.warn(detail);
        this.addingProductId = null;
      },
    });
  }

  private loadCartCount(): void {
    this.cartApi.getMyCart().subscribe({
      next: (cart) => this.cartState.syncFromCart(cart),
      error: () => this.cartState.clear(),
    });
  }

  stockAlertLevel(product: Product): 'ok' | 'warning' | 'critical' {
    if (product.stock <= 0 || product.stock < 3) {
      return 'critical';
    }

    if (product.stock < 5) {
      return 'warning';
    }

    return 'ok';
  }
}
