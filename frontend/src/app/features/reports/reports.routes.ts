import { Routes } from '@angular/router';

export const REPORTS_ROUTES: Routes = [
  {
    path: 'inventory',
    loadComponent: () =>
      import('./pages/inventory-report-page/inventory-report-page.component').then(
        (m) => m.InventoryReportPageComponent
      ),
  },
  {
    path: 'products',
    loadComponent: () =>
      import('./pages/product-management-page/product-management-page.component').then(
        (m) => m.ProductManagementPageComponent
      ),
  },
  {
    path: '',
    pathMatch: 'full',
    redirectTo: 'inventory',
  },
];