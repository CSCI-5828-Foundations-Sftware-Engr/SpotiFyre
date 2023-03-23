import functions_framework
from flask import jsonify

@functions_framework.http
def say_hello(request):

    try:
        params = request.args
        name  = params.get("hello")
        return {'body': {'msg': f"Hey {name}"}}, 200
    except:
        return f"no params found"