import { CanActivateFn, Router } from '@angular/router';
import { inject } from '@angular/core';

import { AuthTokenService } from '../services/auth-token.service';

export const authGuard: CanActivateFn = () => {
  const tokenService = inject(AuthTokenService);
  const router = inject(Router);

  if (tokenService.isAuthenticated()) {
    return true;
  }

  return router.createUrlTree(['/auth/login']);
};
