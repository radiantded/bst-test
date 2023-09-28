from rest_framework import serializers

from customers.models import Customer
from orders.models import Order
from robots.models import Robot


class RobotSerializer(serializers.ModelSerializer):

    class Meta:
        model = Robot
        fields = ('serial', 'model', 'version', 'created')


class OrderSerializer(serializers.ModelSerializer):
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all()
    )

    class Meta:
        model = Order
        fields = ('customer_id', 'robot_serial', )
