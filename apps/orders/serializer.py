from rest_framework import serializers

from apps.orders.models import Order
from apps.tools.models import FarmerSTIR


class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id',
                  'order_num',
                  'order_date',
                  'technique', ]


class OrderStirSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmerSTIR
        fields = ['stir',
                  'full_name',
                  'short_name',
                  'business_type',
                  'business_structure',
                  'legal_address',
                  'postcode',
                  'home_address',
                  'phone_number',
                  'bank_name',
                  'mfo',
                  'payment_account',
                  'director',
                  'director_number',
                  'accountant',
                  'accountant_number', ]


class OrderRetrieveSerializer(serializers.ModelSerializer):
    farmer_stir = OrderStirSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['id',
                  'order_num',
                  'order_date',
                  'technique',
                  'farmer_stir', ]


class OrderCreateSerializer(serializers.ModelSerializer):
    order_date = serializers.DateField(format="%d.%m.%Y", input_formats=['%d.%m.%Y', ])

    class Meta:
        model = Order
        fields = ['farmer_stir',
                  'order_num',
                  'order_date',
                  'operator',
                  'branch_name',
                  'technique', ]
