from rest_framework import serializers
from apps.leasing_agreem.models import LeasingAgreement


class LeasingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeasingAgreement
        fields = ['id',
                  'leasing_num',
                  'leasing_date',
                  'contract_price',
                  'number_of_techs',
                  'lessor_sign',
                  'lessee_sign',
                  'guarantor_sign',
                  'order_model', ]


class LeasingCreateSerializer(serializers.ModelSerializer):
    leasing_date = serializers.DateField(format="%d.%m.%Y", input_formats=['%d.%m.%Y', ])

    class Meta:
        model = LeasingAgreement
        fields = ['leasing_num',
                  'leasing_date',
                  'order_model',
                  'contract_price',
                  'number_of_techs',
                  'order_model', ]
