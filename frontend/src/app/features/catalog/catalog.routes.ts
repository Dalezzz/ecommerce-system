import { Routes } from '@angular/router';

export const CATALOG_ROUTES: Routes = [
  {
    path: '',
    loadComponent: () =>
      import('./pages/catalog-page/catalog-page.component').then((m) => m.CatalogPageComponent),
  },
];
