"""Import all view functions for the JSON server."""

from .orders import (
    retrieve_order,
    list_orders,
    create_order,
    delete_order,
    update_order,
)
from .metals import update_metal, list_metals, retrieve_metal
