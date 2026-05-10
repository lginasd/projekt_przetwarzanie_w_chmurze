# Must be imported even if unused to create according database tables
from app.models.user import User as _
from app.models.order import Order as _
from app.models.product import Product as _
from app.models.order_item import OrderItem as _

print("### init")
