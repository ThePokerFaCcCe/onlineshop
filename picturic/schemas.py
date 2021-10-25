from drf_spectacular.utils import OpenApiExample, OpenApiResponse
from utils.schema_helper import RESPONSE_DEFAULT_RETRIEVE, schema_generator, REQUEST_DEFAULT

PICTURE_GENERIC_RESPONSE = OpenApiExample(
    **RESPONSE_DEFAULT_RETRIEVE,
    value=schema_generator({
        'id': int,
        "file": {
            "image": {
                "url": str,
                "name": str
            },
            "thumbnail": {
                "url": str,
                "name": str
            }
        }
    })
)
