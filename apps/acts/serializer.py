from rest_framework import serializers

from apps.acts.models import Act
from apps.leasing_agreem.models import LeasingAgreement
from apps.orders.models import Order
from apps.technics.models import Technique


class ActTechniqueSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='name.name')

    class Meta:
        model = Technique
        fields = ['id',
                  'name',
                  'model',
                  'price',
                  'prepaid_percent',
                  'prepaid_price', ]


class ActOrderSerializer(serializers.ModelSerializer):
    technique = ActTechniqueSerializer()

    class Meta:
        model = Order
        fields = ['technique', ]


class ActLeasingSerializer(serializers.ModelSerializer):
    order_model = ActOrderSerializer()

    class Meta:
        model = LeasingAgreement
        fields = ['number_of_techs',
                  'contract_price',
                  'order_model', ]


class ActListSerializer(serializers.ModelSerializer):
    leasing_agreem = ActLeasingSerializer()

    class Meta:
        model = Act
        fields = ['id',
                  'act_num',
                  'act_date',
                  'lessor_sign',
                  'lessee_sign',
                  'seller_sign',
                  'seller',
                  'leasing_agreem', ]


class ActCreateSerializer(serializers.ModelSerializer):
    act_date = serializers.DateField(format="%d.%m.%Y", input_formats=['%d.%m.%Y', ])

    class Meta:
        model = Act
        fields = ['act_num',
                  'act_date',
                  'seller',
                  'detected_defects_header',
                  'detected_defects_info',
                  'quality_conclusion_header',
                  'quality_conclusion_info',
                  'leasing_agreem', ]
