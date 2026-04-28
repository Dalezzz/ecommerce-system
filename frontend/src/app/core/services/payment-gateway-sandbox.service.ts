import { Injectable } from '@angular/core';
import { Observable, of, throwError } from 'rxjs';
import { delay } from 'rxjs/operators';

export interface SandboxPaymentData {
  cardHolder: string;
  cardNumber: string;
  expiry: string;
  cvv: string;
  amount: number;
  gateway: 'stripe' | 'mercadopago' | 'paypal';
}

@Injectable({ providedIn: 'root' })
export class PaymentGatewaySandboxService {
  authorizePayment(data: SandboxPaymentData): Observable<{ approved: true; authorizationCode: string }> {
    const cleanedNumber = data.cardNumber.replace(/\s+/g, '');
    const hasEnoughDigits = cleanedNumber.length >= 12 && cleanedNumber.length <= 19;
    const validCvv = /^\d{3,4}$/.test(data.cvv);
    const validExpiry = /^(0[1-9]|1[0-2])\/(\d{2})$/.test(data.expiry);

    if (!data.cardHolder.trim() || !hasEnoughDigits || !validCvv || !validExpiry) {
      return throwError(() => new Error('Datos de tarjeta invalidos'));
    }

    const approved = cleanedNumber.endsWith('1111') || cleanedNumber.startsWith('4242');

    if (!approved) {
      return throwError(() => new Error('Tarjeta rechazada en sandbox'));
    }

    return of({ approved: true as const, authorizationCode: `AUTH-${Math.random().toString(36).slice(2, 10).toUpperCase()}` }).pipe(delay(900));
  }
}