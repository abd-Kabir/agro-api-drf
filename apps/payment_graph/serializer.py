from rest_framework import serializers

from apps.acts.models import Act
from apps.leasing_agreem.models import LeasingAgreement
from apps.orders.models import Order
from apps.payment_graph.models import PaymentGraph, PaymentTable
from apps.technics.models import Technique


class OrderTechnique(serializers.ModelSerializer):
    name = serializers.CharField(source='name.name')

    class Meta:
        model = Technique
        fields = ['id',
                  'name',
                  'model',
                  'price',
                  'yearly_leasing_percent',
                  'leasing_term',
                  'prepaid_percent',
                  'prepaid_price', ]


class LeasingOrder(serializers.ModelSerializer):
    technique = OrderTechnique()

    class Meta:
        model = Order
        fields = ['id',
                  'technique', ]


class ActLeasing(serializers.ModelSerializer):
    order_model = LeasingOrder()

    class Meta:
        model = LeasingAgreement
        fields = ['id',
                  'contract_price',
                  'order_model', ]


class PaymentAct(serializers.ModelSerializer):
    leasing_agreem = ActLeasing()

    class Meta:
        model = Act
        fields = ['id',
                  'act_date',
                  'leasing_agreem', ]


class PaymentGraphSerializer(serializers.ModelSerializer):
    act = PaymentAct()

    class Meta:
        model = PaymentGraph
        fields = ['id',
                  'act', ]


class PaymentTableSerializer(serializers.ModelSerializer):
    payment_graph = PaymentGraphSerializer()

    class Meta:
        model = PaymentTable
        fields = ['id',
                  'residual_amount',
                  'date',
                  'days_count',
                  'quarterly_lease_term_part_of_value',
                  'quarterly_percent_lease_term_payment',
                  'quarterly_lease_term_payment',
                  'is_paid',
                  'payment_graph', ]


class PaymentGraphCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentGraph
        fields = ['id',
                  'act', ]


class OrderTechniqueListFirst(serializers.ModelSerializer):
    name = serializers.CharField(source='name.name')

    class Meta:
        model = Technique
        fields = ['id',
                  'name',
                  'model',
                  'price',
                  'prepaid_percent',
                  'prepaid_price', ]


class LeasingOrderListFirst(serializers.ModelSerializer):
    technique = OrderTechniqueListFirst()

    class Meta:
        model = Order
        fields = ['id',
                  'technique', ]


class ActLeasingListFirst(serializers.ModelSerializer):
    order_model = LeasingOrderListFirst()

    class Meta:
        model = LeasingAgreement
        fields = ['id',
                  'leasing_num',
                  'leasing_date',
                  'contract_price',
                  'number_of_techs',
                  'order_model', ]


class PaymentActListFirst(serializers.ModelSerializer):
    leasing_agreem = ActLeasingListFirst()

    class Meta:
        model = Act
        fields = ['id',
                  'leasing_agreem', ]


class PaymentGraphFirstSerializer(serializers.ModelSerializer):
    act = PaymentActListFirst()

    class Meta:
        model = PaymentGraph
        fields = ['id',
                  'act', ]
