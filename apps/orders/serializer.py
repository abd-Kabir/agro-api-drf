from rest_framework import serializers

from apps.orders.models import Order


class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id',
                  'order_num',
                  'order_date',
                  'technique', ]


class OrderCreateSerializer(serializers.ModelSerializer):
    order_date = serializers.DateField(format="%d.%m.%Y", input_formats=['%d.%m.%Y', ])

    class Meta:
        model = Order
        fields = ['stir',
                  'fullname',
                  'activity_type',
                  'organizational_legal_form',
                  'legal_address',
                  'postal_code',
                  'home_address',
                  'phone_num',
                  'mfo',
                  'account_num',
                  'bank_name',
                  'chief_name',
                  'chief_phone_num',
                  'accountant_name',
                  'accountant_phone_num',
                  'order_num',
                  'order_date',
                  'branch_name',
                  'technique', ]
