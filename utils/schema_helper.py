from typing import Any


RESPONSE_DEFAULT_RETRIEVE = {
    'name': 'Response Retrieve',
    'response_only': True,
}
RESPONSE_DEFAULT_LIST = {
    'name': 'Response List',
    'response_only': True,
}
REQUEST_DEFAULT = {
    'name': 'Request',
    'request_only': True,
}
def convert_type_to_value(vtype) -> Any:
    if isinstance(vtype, type):
        if issubclass(vtype, bool):
            return True
        if issubclass(vtype, int):
            return 0
        if issubclass(vtype, float):
            return 0.0
        if issubclass(vtype, str):
            return 'string'
        if issubclass(vtype, (list, tuple, set)):
            return []

    else:
        if isinstance(vtype, str):
            if vtype == '+int':
                return 4294967295

    return vtype


def convert_list(data: list):
    converted_items = []
    for item in data:
        if isinstance(item, dict):
            converted = schema_generator(item)
        elif isinstance(item, (list, tuple, set)):
            converted = convert_list(item)
        else:
            converted = convert_type_to_value(item)
        converted_items.append(converted)
    return converted_items


def schema_generator(data: dict):
    for k, v in data.items():

        if isinstance(v, dict):
            data[k] = schema_generator(v)

        elif isinstance(v, (list, tuple, set)):
            data[k] = convert_list(v)

        else:
            data[k] = convert_type_to_value(v)

    return data


PAGINATION_DEFAULT=schema_generator({
            "count": int,
            "next": str,
            "previous": str,
        })