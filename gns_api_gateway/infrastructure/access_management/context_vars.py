import contextvars

__all__ = ["user"]

user: contextvars.ContextVar[str] = contextvars.ContextVar("user")
