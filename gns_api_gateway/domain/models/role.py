from enum import Enum

__all__ = ["UserRole"]


class UserRole(int, Enum):
    STUDENT = 1
    TEACHER = 2
