from flask import request
with app.test_request_context('/test/hello', method='POST'):
    assert request.path == '/test/hello'
    assert request.method == 'POST'