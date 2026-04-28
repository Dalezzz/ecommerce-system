import { Injectable } from '@angular/core';
import { signal } from '@angular/core';

export interface AppNotification {
  type: 'info' | 'warn' | 'error' | 'success';
  message: string;
}

@Injectable({ providedIn: 'root' })
export class NotificationService {
  private readonly state = signal<AppNotification | null>(null);
  readonly current = this.state.asReadonly();

  private timeoutId: number | null = null;

  info(message: string): void {
    this.push('info', message);
  }

  success(message: string): void {
    this.push('success', message);
  }

  warn(message: string): void {
    this.push('warn', message);
  }

  error(message: string): void {
    this.push('error', message);
  }

  clear(): void {
    this.state.set(null);
  }

  private push(type: AppNotification['type'], message: string): void {
    if (this.timeoutId !== null) {
      clearTimeout(this.timeoutId);
    }

    this.state.set({ type, message });
    this.timeoutId = window.setTimeout(() => {
      this.state.set(null);
      this.timeoutId = null;
    }, 3500);
  }
}
