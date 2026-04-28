import { Component } from '@angular/core';

import { NotificationService } from '../../../../core/services/notification.service';
import { InventoryReportItem, ReportsApiService } from '../../../../core/services/reports-api.service';

@Component({
  selector: 'app-inventory-report-page',
  standalone: true,
  templateUrl: './inventory-report-page.component.html',
  styleUrl: './inventory-report-page.component.scss',
})
export class InventoryReportPageComponent {
  items: InventoryReportItem[] = [];
  loading = true;
  errorMessage: string | null = null;
  onlyCritical = false;

  constructor(
    private readonly reportsApi: ReportsApiService,
    private readonly notifier: NotificationService
  ) {}

  ngOnInit(): void {
    this.loadReport();
  }

  loadReport(): void {
    this.loading = true;
    this.errorMessage = null;

    this.reportsApi.inventory({ solo_criticos: this.onlyCritical }).subscribe({
      next: (items) => {
        this.items = items;
        this.loading = false;
      },
      error: (error) => {
        this.errorMessage = error?.error?.detail ?? 'No fue posible cargar el reporte de inventario';
        this.loading = false;
      },
    });
  }

  toggleOnlyCritical(checked: boolean): void {
    this.onlyCritical = checked;
    this.loadReport();
  }

  exportCsv(): void {
    const header = ['sku', 'nombre', 'categoria', 'stock_actual', 'stock_minimo', 'umbral_critico', 'estado'];
    const rows = this.items.map((item) => [
      item.sku,
      item.nombre,
      item.categoria ?? '',
      item.stock_actual,
      item.stock_minimo,
      item.umbral_critico,
      item.estado,
    ]);

    const csv = [header, ...rows]
      .map((row) => row.map((value) => `"${String(value).replace(/"/g, '""')}"`).join(','))
      .join('\n');

    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'reporte-inventario.csv';
    link.click();
    URL.revokeObjectURL(url);

    this.notifier.info('Reporte exportado en CSV');
  }
}