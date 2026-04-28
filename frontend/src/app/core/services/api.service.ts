import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { HttpParams } from '@angular/common/http';

import { API_BASE_URL } from '../constants/api.constants';

@Injectable({ providedIn: 'root' })
export class ApiService {
  constructor(private readonly http: HttpClient) {}

  get<T>(path: string, params?: Record<string, string | number | boolean | null | undefined>) {
    const httpParams = new HttpParams({
      fromObject: Object.entries(params ?? {}).reduce<Record<string, string>>((acc, [key, value]) => {
        if (value !== null && value !== undefined && value !== '') {
          acc[key] = String(value);
        }
        return acc;
      }, {}),
    });

    return this.http.get<T>(`${API_BASE_URL}${path}`, { params: httpParams });
  }

  post<T>(path: string, body: unknown) {
    return this.http.post<T>(`${API_BASE_URL}${path}`, body);
  }

  put<T>(path: string, body: unknown) {
    return this.http.put<T>(`${API_BASE_URL}${path}`, body);
  }

  delete<T>(path: string) {
    return this.http.delete<T>(`${API_BASE_URL}${path}`);
  }
}
