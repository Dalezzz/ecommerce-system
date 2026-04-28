import { Injectable, signal } from '@angular/core';

import { AUTH_TOKEN_KEY } from '../constants/api.constants';

@Injectable({ providedIn: 'root' })
export class AuthTokenService {
  private readonly tokenState = signal<string | null>(localStorage.getItem(AUTH_TOKEN_KEY));

  readonly token = this.tokenState.asReadonly();

  getToken(): string | null {
    return this.tokenState();
  }

  setToken(token: string): void {
    localStorage.setItem(AUTH_TOKEN_KEY, token);
    this.tokenState.set(token);
  }

  clearToken(): void {
    localStorage.removeItem(AUTH_TOKEN_KEY);
    this.tokenState.set(null);
  }

  getRole(): string | null {
    const token = this.tokenState();
    if (!token) {
      return null;
    }

    const payload = this.decodePayload(token);
    const role = payload?.['rol'];
    return typeof role === 'string' ? role : null;
  }

  isAuthenticated(): boolean {
    return !!this.tokenState();
  }

  private decodePayload(token: string): Record<string, unknown> | null {
    const parts = token.split('.');
    if (parts.length < 2) {
      return null;
    }

    try {
      const base64 = parts[1].replace(/-/g, '+').replace(/_/g, '/');
      const padded = base64.padEnd(Math.ceil(base64.length / 4) * 4, '=');
      return JSON.parse(atob(padded)) as Record<string, unknown>;
    } catch {
      return null;
    }
  }
}
