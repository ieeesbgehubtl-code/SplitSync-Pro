from rest_framework.response import Response

def ok(data=None, status=200, meta=None):
    payload = {'success': True, 'data': data if data is not None else {}}
    if meta is not None: payload['meta'] = meta
    return Response(payload, status=status)
