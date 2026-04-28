import { Injectable } from '@angular/core';

import { Observable } from 'rxjs';

import { ApiService } from './api.service';

export interface InventoryReportItem {
  producto_id: number;
  sku: string;
  nombre: string;
  categoria: string | null;
  stock_actual: number;
  stock_minimo: number;
  umbral_critico: number;
  estado: 'ok' | 'warning' | 'critical';
  color: 'green' | 'yellow' | 'red';
}

@Injectable({ providedIn: 'root' })
export class ReportsApiService {
  constructor(private readonly api: ApiService) {}

  inventory(params: { categoria_id?: number; solo_criticos?: boolean } = {}): Observable<InventoryReportItem[]> {
    return this.api.get<InventoryReportItem[]>('/reports/inventory', params);
  }
}