from rest_framework import serializers

from apps.expert_assessment.models import ExpertAssessment


class ExpertAssessmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpertAssessment
        fields = ['id',
                  'guarantors_count',
                  'order_model',
                  'branch_name', ]
