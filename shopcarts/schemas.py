from drf_spectacular.utils import OpenApiExample
from products.schemas import SIMPLE_PRODUCT_RETRIEVE
from utils.schema_helper import RESPONSE_DEFAULT_LIST, RESPONSE_DEFAULT_RETRIEVE, schema_generator

CARTITEM_RESPONSE_RETRIEVE = OpenApiExample(
    **RESPONSE_DEFAULT_RETRIEVE,
    value={
        **schema_generator({
            'quantity': "+int",
            'total_price': int,
        }),
        'product': SIMPLE_PRODUCT_RETRIEVE.value
    }
)

CART_RESPONSE_RETRIEVE = OpenApiExample(
    **RESPONSE_DEFAULT_RETRIEVE,
    value={
        **schema_generator({
            'id': "uuid",
            'total_price': int,
        }),
        'products': [CARTITEM_RESPONSE_RETRIEVE.value]
    }
)
