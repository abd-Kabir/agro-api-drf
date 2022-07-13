from rest_framework import serializers

from apps.guarantee_agreem.models import Guarantor, GuaranteeAgreement


class GuaranteeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuaranteeAgreement
        fields = ['guarantee_num',
                  'guarantee_date',
                  'leasing_agreem', ]


class GuarantorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guarantor
        fields = ['id',
                  'farmer_stir',
                  'guarantee_agreem', ]
