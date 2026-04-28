import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Product, Category } from '../../../../core/models/product.model';
import { ProductsApiService } from '../../../../core/services/products-api.service';
import { NotificationService } from '../../../../core/services/notification.service';

@Component({
  selector: 'app-product-management-page',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './product-management-page.component.html',
  styleUrl: './product-management-page.component.scss'
})
export class ProductManagementPageComponent implements OnInit {
  products: Product[] = [];
  categories: Category[] = [];
  loading = true;
  editingProduct: Partial<Product> | null = null;
  isNewProduct = false;

  constructor(
    private productsApi: ProductsApiService,
    private notifier: NotificationService
  ) {}

  ngOnInit(): void {
    this.loadProducts();
    this.loadCategories();
  }

  loadProducts(): void {
    this.loading = true;
    this.productsApi.list().subscribe({
      next: (products) => {
        this.products = products;
        this.loading = false;
      },
      error: () => {
        this.notifier.error('Error al cargar productos');
        this.loading = false;
      }
    });
  }

  loadCategories(): void {
    this.productsApi.getCategories().subscribe({
      next: (categories) => this.categories = categories
    });
  }

  startNewProduct(): void {
    this.isNewProduct = true;
    this.editingProduct = {
      nombre: '',
      sku: '',
      descripcion: '',
      precio: 0,
      stock: 0,
      categoria_id: this.categories.length > 0 ? this.categories[0].id : 0,
      activo: true
    };
  }

  editProduct(product: Product): void {
    this.isNewProduct = false;
    this.editingProduct = { ...product };
  }

  cancelEdit(): void {
    this.editingProduct = null;
  }

  saveProduct(): void {
    if (!this.editingProduct) return;

    if (this.isNewProduct) {
      this.productsApi.create(this.editingProduct).subscribe({
        next: () => {
          this.notifier.success('Producto creado con éxito');
          this.editingProduct = null;
          this.loadProducts();
        },
        error: (err) => this.notifier.error(err?.error?.detail || 'Error al crear producto')
      });
    } else {
      const id = (this.editingProduct as Product).id;
      this.productsApi.update(id, this.editingProduct).subscribe({
        next: () => {
          this.notifier.success('Producto actualizado con éxito');
          this.editingProduct = null;
          this.loadProducts();
        },
        error: (err) => this.notifier.error(err?.error?.detail || 'Error al actualizar producto')
      });
    }
  }

  deleteProduct(id: number): void {
    if (confirm('¿Estás seguro de que deseas eliminar (desactivar) este producto?')) {
      this.productsApi.delete(id).subscribe({
        next: () => {
          this.notifier.success('Producto desactivado');
          this.loadProducts();
        },
        error: () => this.notifier.error('Error al eliminar producto')
      });
    }
  }
}
