from enum import Enum


class OrderStatus(str, Enum):
    PENDING = "pending"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
