from drf_spectacular.utils import OpenApiExample
from utils.schema_helper import RESPONSE_DEFAULT_LIST, RESPONSE_DEFAULT_RETRIEVE, schema_generator


_base_comment = {
    "id": int,
    "reply_to": int,
    "text": str,
    "hidden": bool,
    "user": int,
    "created_at": "datetime",
    "updated_at": "datetime",
}

COMMENT_RESPONSE_RETRIEVE = OpenApiExample(
    **RESPONSE_DEFAULT_RETRIEVE,
    value=schema_generator({
        **_base_comment,
        "replies": [
            {
                **_base_comment,
                'replies': ['...']
            }
        ],
    })
)

COMMENT_RESPONSE_LIST = OpenApiExample(
    **RESPONSE_DEFAULT_LIST,
    value=[COMMENT_RESPONSE_RETRIEVE.value]
)
