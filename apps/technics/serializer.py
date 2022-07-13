from rest_framework import serializers

from apps.technics.models import Technique, TechniqueName, TechniqueType


class TechnicsEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Technique
        fields = ['id',
                  'type',
                  'name',
                  'model',
                  'manufacturer',
                  'guarantors_num',  # TODO: buni olib tashlash kere bo'ladi keyinchalik
                  'price',
                  'yearly_leasing_percent',
                  'leasing_term',
                  'subsidy',
                  'prepaid_percent', ]


class TechnicsListSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='name.name')
    type = serializers.CharField(source='type.name')

    class Meta:
        model = Technique
        fields = ['id',
                  'type',
                  'name',
                  'model',
                  'manufacturer',
                  'country_name',
                  'leasing_term',
                  'prepaid_percent',
                  'prepaid_price',
                  'price',
                  'yearly_leasing_percent',
                  'subsidy',
                  'guarantors_num',
                  'guarantee_bail',
                  'insurance', ]


class TechnicsCompanyListSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='name.name')
    type = serializers.CharField(source='type.name')

    class Meta:
        model = Technique
        fields = ['id',
                  'type',
                  'name',
                  'model',
                  'manufacturer',
                  'country_name',
                  'leasing_term',
                  'prepaid_percent',
                  'price',
                  'yearly_leasing_percent',
                  'subsidy',
                  'guarantee_bail',
                  'insurance', ]


class TechnicsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Technique
        fields = ['type',
                  'name',
                  'model',
                  'manufacturer',
                  'country_name',
                  'leasing_term',
                  'prepaid_percent',
                  'price',
                  'yearly_leasing_percent',
                  'subsidy',
                  'guarantors_num',
                  'guarantee_bail',
                  'insurance', ]


class TechnicsUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Technique
        fields = ['name',
                  'type',
                  'model',
                  'manufacturer',
                  'country_name',
                  'leasing_term',
                  'prepaid_percent',
                  'price',
                  'yearly_leasing_percent',
                  'subsidy',
                  'guarantors_num',
                  'guarantee_bail',
                  'insurance', ]


class TechnicsNamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechniqueName
        fields = ['type',
                  'name', ]


class TechnicsTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechniqueType
        fields = ['name', ]
