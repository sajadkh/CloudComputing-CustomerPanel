from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('/info', views.info, name='Get User Info'),
    path('/order', views.order_req, name='Order'),
    path('/order/<int:order_id>', views.get_order_detail, name='Get Order Details')
]
