import { CanActivateFn, Router } from '@angular/router';
import { inject } from '@angular/core';

import { AuthTokenService } from '../services/auth-token.service';

export const adminGuard: CanActivateFn = () => {
  const tokenService = inject(AuthTokenService);
  const router = inject(Router);

  if (tokenService.isAuthenticated() && tokenService.getRole() === 'admin') {
    return true;
  }

  return tokenService.isAuthenticated() ? router.createUrlTree(['/catalog']) : router.createUrlTree(['/auth/login']);
};