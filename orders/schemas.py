from drf_spectacular.utils import OpenApiExample
from orders.models import Order
from products.schemas import SIMPLE_PRODUCT_RETRIEVE
from utils.schema_helper import RESPONSE_DEFAULT_LIST, RESPONSE_DEFAULT_RETRIEVE, schema_generator


SIMPLE_POSTTYPE_RESPONSE_RETRIEVE = OpenApiExample(
    **RESPONSE_DEFAULT_RETRIEVE,
    value=schema_generator({
        'id': int,
        'title': str,
    })
)


ORDERITEM_RESPONSE_RETRIEVE = OpenApiExample(
    **RESPONSE_DEFAULT_RETRIEVE,
    value={
        **schema_generator({
            'quantity': "+int",
            'price': int,
            'total_price': int,
        }),
        'product': SIMPLE_PRODUCT_RETRIEVE.value
    }
)


ORDERITEM_RESPONSE_LIST = OpenApiExample(
    **RESPONSE_DEFAULT_LIST,
    value=[ORDERITEM_RESPONSE_RETRIEVE.value]
)


ORDER_RESPONSE_RETRIEVE = OpenApiExample(
    **RESPONSE_DEFAULT_RETRIEVE,
    value={
        **schema_generator({
            'id': int,
            'first_name': str,
            'last_name': str,
            'phone_number': str,
            'email': 'email',

            'post_type': SIMPLE_POSTTYPE_RESPONSE_RETRIEVE.value,
            'post_type_price': int,
            'country': "country",
            'city': str,
            'street': str,
            'postal_code': str,

            'total_price': int,
            'buy_token': str,

            'status': Order.OrderStatus.WAITING,
            'user': int,
        }),
        'products': ORDERITEM_RESPONSE_LIST.value
    }
)


ORDER_RESPONSE_LIST = OpenApiExample(
    **RESPONSE_DEFAULT_LIST,
    value=[ORDER_RESPONSE_RETRIEVE.value]
)
