import { ChangeDetectionStrategy, Component } from '@angular/core';
import { NgIf } from '@angular/common';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { finalize } from 'rxjs';

import { AuthApiService } from '../../../../core/services/auth-api.service';
import { AuthTokenService } from '../../../../core/services/auth-token.service';

@Component({
  selector: 'app-login-page',
  standalone: true,
  imports: [NgIf, ReactiveFormsModule],
  templateUrl: './login-page.component.html',
  styleUrl: './login-page.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class LoginPageComponent {
  isSubmitting = false;
  errorMessage: string | null = null;

  readonly form = this.fb.nonNullable.group({
    email: ['', [Validators.required, Validators.email]],
    password: ['', [Validators.required, Validators.minLength(8)]],
  });

  constructor(
    private readonly fb: FormBuilder,
    private readonly authApi: AuthApiService,
    private readonly tokenService: AuthTokenService,
    private readonly router: Router
  ) {}

  submit(): void {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    this.isSubmitting = true;
    this.errorMessage = null;

    const { email, password } = this.form.getRawValue();
    this.authApi
      .login(email, password)
      .pipe(finalize(() => (this.isSubmitting = false)))
      .subscribe({
        next: (response) => {
          this.tokenService.setToken(response.access_token);
          this.router.navigate(['/catalog']);
        },
        error: (error) => {
          this.errorMessage = error?.error?.detail ?? 'No fue posible iniciar sesion';
        },
      });
  }
}
