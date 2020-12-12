import requests
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils.crypto import get_random_string, hashlib
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

import json

# Create your views here.
from appCustomer import response
from appCustomer.exceptions import RequestException
from appCustomer.models import Order
from appCustomer.serializers import OrderSerializer, OrderRequestSerializer

PANEL_TOKEN = "Y3VzdG9tZXI6Y3VzdG9tZXJAbG9jYWwuY29tOklOVEVSTkFMOjk5OTk5OQ=="


def token_validation(token):
    r = requests.post("http://authentication:8000/auth/verify", data={}, headers={"token": token})
    if r.status_code == 200:
        info = r.json()['data']
        return info
    else:
        raise Exception("Token is invalid")


def extract_request_data_post(request):
    try:
        if len(request.POST.keys()) > 0:
            request_data = request.POST
        else:
            request_data = json.load(request)
        return request_data
    except:
        return {}


def extract_request_headers(request):
    request_data = request.headers
    return request_data


def validate_required_body_items(required_fields, request_data):
    errors = []
    for item in required_fields:
        if item not in request_data.keys():
            errors.append(item + " is required!")

    return errors


def validate_required_header_items(required_fields, request_headers):
    errors = []
    for item in required_fields:
        if item not in request_headers.keys():
            errors.append(item + " is required!")

    return errors


@csrf_exempt
def info(request):
    if request.method == "GET":
        # Validate Header
        request_headers = extract_request_headers(request)
        required_headers_fields = ["token"]
        errors = validate_required_header_items(required_headers_fields, request_headers)
        if len(errors) > 0:
            return response.bad_request_response(errors)
        info = token_validation(request_headers["token"])
        del info['id']
        if info['role'] != "CUSTOMER":
            return response.forbidden_response()
        return response.success_response(info)
    return response.method_not_allowed_response()


def request_order(restaurant, customer, foods_list):
    r = requests.post("http://restaurant:8001/restaurants/" + restaurant + "/order",
                      data={'foods': foods_list, 'customer': customer}, headers={"token": PANEL_TOKEN})
    if r.status_code == 200:
        order = r.json()['data']
        return order
    elif r.status_code == 400 or r.status_code == 404:
        raise RequestException(r.status_code, r.json()['error'])
    else:
        raise Exception("Order Failed!")


def get_order(restaurant, order_id):
    r = requests.get("http://restaurant:8001/restaurants/" + restaurant + "/order/" + str(order_id),
                     data={}, headers={"token": PANEL_TOKEN})
    if r.status_code == 200:
        order = r.json()['data']
        return order
    elif r.status_code == 400 or r.status_code == 404:
        raise RequestException(r.status_code, r.json()['error'])
    else:
        raise Exception("Get Order Failed!")


@csrf_exempt
def order_req(request):
    if request.method == 'GET':
        try:
            # Validate Header
            request_headers = extract_request_headers(request)
            required_headers_fields = ["token"]
            errors = validate_required_header_items(required_headers_fields, request_headers)
            if len(errors) > 0:
                return response.bad_request_response(errors)
            info = token_validation(request_headers['token'])
            if info['role'] != "CUSTOMER":
                return response.forbidden_response()
            orders = Order.objects.filter(customer=info['username'])
            orders_data = []
            for order in orders:
                orders_data.append(OrderRequestSerializer(order).data)
            return response.success_response(orders_data)
        except Exception as e:
            if str(e) == "Token is invalid":
                return response.un_authorized_response()
            elif str(e) == "Order matching query does not exist.":
                return response.success_response([])
            return response.internal_server_error_response()

    if request.method == 'POST':
        try:
            # Validate Header
            request_headers = extract_request_headers(request)
            required_headers_fields = ["token"]
            errors = validate_required_header_items(required_headers_fields, request_headers)
            if len(errors) > 0:
                return response.bad_request_response(errors)

            # Validate Data
            request_data = extract_request_data_post(request)
            required_data_fields = ["restaurant", "foods"]
            errors = validate_required_body_items(required_data_fields, request_data)
            if len(errors) > 0:
                return response.bad_request_response(errors)
            info = token_validation(request_headers['token'])
            if info['role'] != "CUSTOMER":
                return response.forbidden_response()
            restaurant = request_data['restaurant']
            username = info['username']
            order = Order(restaurant=restaurant, customer=username)
            result = request_order(order.restaurant, order.customer, request_data['foods'])
            order.total_price = result["total_price"]
            order.order_id = result["id"]
            order.status = result["status"]
            order.save()
            return response.success_response(OrderRequestSerializer(order).data)
        except Exception as e:
            if str(e) == "Token is invalid":
                return response.un_authorized_response()
            elif str(e) == "Order Failed!":
                return response.internal_server_error_response()
            elif isinstance(e, RequestException):
                if e.status == 404:
                    return response.not_found_response(e.message)
                elif e.status == 400:
                    return response.bad_request_response(e.message)
            else:
                return response.internal_server_error_response()
    return response.internal_server_error_response()


@csrf_exempt
def get_order_detail(request, order_id):
    if request.method == 'GET':
        try:
            # Validate Header
            request_headers = extract_request_headers(request)
            required_headers_fields = ["token"]
            errors = validate_required_header_items(required_headers_fields, request_headers)
            if len(errors) > 0:
                return response.bad_request_response(errors)
            info = token_validation(request_headers['token'])
            if info['role'] != "CUSTOMER":
                return response.forbidden_response()
            order = Order.objects.get(id=order_id)
            order_info = get_order(order.restaurant, order.order_id)
            order.status = order_info["status"]
            order_info["id"] = order.id
            order.save()
            return response.success_response(order_info)
        except Exception as e:
            if str(e) == "Token is invalid":
                return response.un_authorized_response()
            elif str(e) == "Get Order Failed!":
                return response.internal_server_error_response()
            elif str(e) == "Order matching query does not exist.":
                return response.not_found_response("Order Not Found")
            elif isinstance(e, RequestException):
                if e.status == 404:
                    return response.not_found_response(e.message)
                elif e.status == 400:
                    return response.bad_request_response(e.message)
            else:
                return response.internal_server_error_response()
