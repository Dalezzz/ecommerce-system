class DomainError(Exception):
	"""Base domain exception for business rule failures."""

	status_code = 400
	error_code = "domain_error"

	def __init__(self, detail: str):
		self.detail = detail
		super().__init__(detail)

	def to_dict(self) -> dict[str, str]:
		return {
			"error": self.error_code,
			"detail": self.detail,
		}


class ValidationError(DomainError):
	status_code = 400
	error_code = "validation_error"


class AuthenticationError(DomainError):
	status_code = 401
	error_code = "authentication_error"


class ForbiddenError(DomainError):
	status_code = 403
	error_code = "forbidden"


class NotFoundError(DomainError):
	status_code = 404
	error_code = "not_found"


class ConflictError(DomainError):
	status_code = 409
	error_code = "conflict"
