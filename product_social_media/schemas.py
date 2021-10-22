from drf_spectacular.utils import OpenApiExample
from social_media.schemas import TAG_RESPONSE_RETRIEVE
from utils.schema_helper import PAGINATION_DEFAULT, RESPONSE_DEFAULT_LIST, RESPONSE_DEFAULT_RETRIEVE, schema_generator
from products.schemas import PRODUCT_RESPONSE_RETRIEVE

SOCIAL_PRODUCT_RESULT_RETRIEVE = OpenApiExample(
    **RESPONSE_DEFAULT_RETRIEVE,
    value={
        **PRODUCT_RESPONSE_RETRIEVE.value,
        'tags': [TAG_RESPONSE_RETRIEVE.value],
        **schema_generator({
            "likes": int,
            "liked_by_user": bool,
            "comments_count": int,
        })}
)

SOCIAL_PRODUCT_RESULT_LIST = OpenApiExample(
    **RESPONSE_DEFAULT_LIST,
    value={
        **PAGINATION_DEFAULT,
        "results": [PRODUCT_RESPONSE_RETRIEVE.value]
    }
)
