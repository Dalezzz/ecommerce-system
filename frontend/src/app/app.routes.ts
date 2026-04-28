import { Routes } from '@angular/router';
import { authGuard } from './core/guards/auth.guard';
import { adminGuard } from './core/guards/admin.guard';

export const routes: Routes = [
	{
		path: 'auth',
		loadChildren: () => import('./features/auth/auth.routes').then((m) => m.AUTH_ROUTES),
	},
	{
		path: 'catalog',
		loadChildren: () =>
			import('./features/catalog/catalog.routes').then((m) => m.CATALOG_ROUTES),
	},
	{
		path: 'cart',
		loadChildren: () => import('./features/cart/cart.routes').then((m) => m.CART_ROUTES),
	},
	{
		path: 'orders',
		canActivate: [authGuard],
		loadChildren: () => import('./features/orders/orders.routes').then((m) => m.ORDERS_ROUTES),
	},
	{
		path: 'admin',
		canActivate: [adminGuard],
		loadChildren: () => import('./features/reports/reports.routes').then((m) => m.REPORTS_ROUTES),
	},
	{
		path: '',
		pathMatch: 'full',
		redirectTo: 'catalog',
	},
	{
		path: '**',
		redirectTo: 'catalog',
	},
];
