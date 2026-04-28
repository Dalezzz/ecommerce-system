import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';

import { Observable } from 'rxjs';

import { API_BASE_URL } from '../constants/api.constants';
import { AuthTokenResponse } from '../models/auth.model';

@Injectable({ providedIn: 'root' })
export class AuthApiService {
  constructor(private readonly http: HttpClient) {}

  login(email: string, password: string): Observable<AuthTokenResponse> {
    const body = new HttpParams()
      .set('username', email)
      .set('password', password)
      .toString();

    return this.http.post<AuthTokenResponse>(`${API_BASE_URL}/auth/login`, body, {
      headers: new HttpHeaders({
        'Content-Type': 'application/x-www-form-urlencoded',
      }),
    });
  }
}
