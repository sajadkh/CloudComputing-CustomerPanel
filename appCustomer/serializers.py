from rest_framework import serializers
from .models import Order


class OrderRequestSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    status = serializers.CharField(max_length=255)
    restaurant = serializers.CharField(max_length=255)
    total_price = serializers.FloatField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class OrderSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        order = Order.objects.create(
            order_id=validated_data['order_id'],
            status=validated_data['status'],
            restaurant=validated_data['restaurant'],
            customer=validated_data['customer'],
            total_price=validated_data['total_price']
        )
        order.save()
        return order

    class Meta:
        model = Order
        fields = ['id', 'order_id', 'status', 'restaurant', 'customer', 'total_price']
