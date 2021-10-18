from rest_framework.viewsets import ModelViewSet

def all_methods(*except_methods, **kwargs):
    use_only = kwargs.get('only', None)
    if use_only:
        req_methods = ['put', 'post', 'patch', 'delete', 'get']
        req_methods.remove(use_only.lower())
        except_methods = req_methods

    methods = ModelViewSet.http_method_names
    return [m for m in methods if m not in except_methods] if except_methods else methods

