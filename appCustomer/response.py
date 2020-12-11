from datetime import datetime

from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse


def success_response(data):
    return JsonResponse({
        "data": data,
        "status": "success",
        "timestamp": round(datetime.now().timestamp())
    }, encoder=DjangoJSONEncoder, status=200)


def bad_request_response(error):
    return JsonResponse({
        "error": error,
        "status": "error",
        "timestamp": round(datetime.now().timestamp())
    }, encoder=DjangoJSONEncoder, status=400)


def un_authorized_response():
    return JsonResponse({
        "error": "UnAuthorized Error",
        "status": "error",
        "timestamp": round(datetime.now().timestamp())
    }, encoder=DjangoJSONEncoder, status=401)


def forbidden_response():
    return JsonResponse({
        "error": "Forbidden",
        "status": "error",
        "timestamp": round(datetime.now().timestamp())
    }, encoder=DjangoJSONEncoder, status=404)


def not_found_response(error):
    return JsonResponse({
        "error": error,
        "status": "error",
        "timestamp": round(datetime.now().timestamp())
    }, encoder=DjangoJSONEncoder, status=404)


def method_not_allowed_response():
    return JsonResponse({
        "error": "Method Not Allowed",
        "status": "error",
        "timestamp": round(datetime.now().timestamp())
    }, encoder=DjangoJSONEncoder, status=406)


def internal_server_error_response():
    return JsonResponse({
        "error": "Internal Server Error",
        "status": "error",
        "timestamp": round(datetime.now().timestamp())
    }, encoder=DjangoJSONEncoder, status=500)
