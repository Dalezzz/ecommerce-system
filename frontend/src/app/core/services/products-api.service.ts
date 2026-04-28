import { Injectable } from '@angular/core';

import { Observable } from 'rxjs';

import { Product, Category } from '../models/product.model';
import { ApiService } from './api.service';

@Injectable({ providedIn: 'root' })
export class ProductsApiService {
  constructor(private readonly api: ApiService) {}

  list(search?: string, categoryId?: number): Observable<Product[]> {
    let url = '/products/';
    const params: any = {};
    if (search) params.search = search;
    if (categoryId) params.category_id = categoryId;
    return this.api.get<Product[]>(url, params);
  }

  getCategories(): Observable<Category[]> {
    return this.api.get<Category[]>('/products/categories');
  }

  create(product: Partial<Product>): Observable<Product> {
    return this.api.post<Product>('/products/', product);
  }

  update(id: number, product: Partial<Product>): Observable<Product> {
    return this.api.put<Product>(`/products/${id}`, product);
  }

  delete(id: number): Observable<Product> {
    return this.api.delete<Product>(`/products/${id}`);
  }
}
