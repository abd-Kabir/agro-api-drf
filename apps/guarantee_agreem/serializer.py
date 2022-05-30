from rest_framework import serializers
from apps.guarantee_agreem.models import GuaranteeAgreement


class GuaranteeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuaranteeAgreement
        fields = ['id',
                  'guarantors_signed_count',
                  'guarantor',
                  'leasing_agreem', ]
