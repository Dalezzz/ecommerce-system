import { HttpErrorResponse, HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { Router } from '@angular/router';
import { catchError, throwError } from 'rxjs';

import { AuthTokenService } from '../services/auth-token.service';
import { NotificationService } from '../services/notification.service';

export const httpErrorInterceptor: HttpInterceptorFn = (req, next) => {
  const notifier = inject(NotificationService);
  const router = inject(Router);
  const tokenService = inject(AuthTokenService);

  return next(req).pipe(
    catchError((error: HttpErrorResponse) => {
      if (error.status === 401) {
        tokenService.clearToken();
        notifier.warn('Tu sesion ha expirado. Inicia sesion nuevamente.');
        router.navigate(['/auth/login']);
      } else if (error.status >= 500) {
        notifier.error('Error interno del servidor. Intenta nuevamente.');
      } else {
        notifier.warn(error.error?.detail ?? 'No fue posible completar la solicitud.');
      }

      return throwError(() => error);
    })
  );
};
