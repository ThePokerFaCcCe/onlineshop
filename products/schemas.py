from drf_spectacular.utils import OpenApiExample
from picturic.schemas import PICTURE_GENERIC_RESPONSE
from utils.schema_helper import PAGINATION_DEFAULT, REQUEST_DEFAULT, RESPONSE_DEFAULT_LIST, RESPONSE_DEFAULT_RETRIEVE, schema_generator

PROMOTION_REQUEST = OpenApiExample(
    **REQUEST_DEFAULT,
    value=schema_generator({
        "description": str,
        "discount": 99.99
    })
)

PROMOTION_RESPONSE_RETRIEVE = OpenApiExample(
    **RESPONSE_DEFAULT_RETRIEVE,
    value=schema_generator({
        'id': int,
        "description": str,
        "discount": 99.99
    })
)

PROMOTION_RESPONSE_LIST = OpenApiExample(
    **RESPONSE_DEFAULT_LIST,
    value=[PROMOTION_RESPONSE_RETRIEVE.value]
)


SIMPLE_PRODUCT_RETRIEVE = OpenApiExample(
    **RESPONSE_DEFAULT_RETRIEVE,
    value=schema_generator({
        "id": int,
        "title": str,
        "description": str,
        "pictures": [PICTURE_GENERIC_RESPONSE.value],
        "price": '+int',
    })
)


PRODUCT_RESPONSE_RETRIEVE = OpenApiExample(
    **RESPONSE_DEFAULT_RETRIEVE,
    value={
        **SIMPLE_PRODUCT_RETRIEVE.value,
        **schema_generator({
            "inventory": '+int',
            "category": {
                'id': int,
                'title': str,
                'description': str,
            },
            "promotions": [PROMOTION_RESPONSE_RETRIEVE.value]
        })
    }
)

PRODUCT_RESPONSE_LIST = OpenApiExample(
    **RESPONSE_DEFAULT_LIST,
    value={
        **PAGINATION_DEFAULT,
        "results": [PRODUCT_RESPONSE_RETRIEVE.value]
    }
)


CATEGORY_RESPONSE_RETRIEVE = OpenApiExample(
    **RESPONSE_DEFAULT_RETRIEVE,
    value=schema_generator({
        'id': int,
        'title': str,
        'description': str,
        'featured_product': {k: v for k, v in PRODUCT_RESPONSE_RETRIEVE.value.items() if k != 'category'}
    })
)

CATEGORY_RESPONSE_LIST = OpenApiExample(
    **RESPONSE_DEFAULT_LIST,
    value=[CATEGORY_RESPONSE_RETRIEVE.value]
)
