from django.urls import path

from apps.expert_assessment.views import ExpertAssessmentCreateAPIView, ExpertAssessmentCompanyProvinceListAPIView, \
    ExpertAssessmentCompanyDistrictListAPIView, ExpertAssessmentCompanyListAPIView

app_name = 'expert-assessment'
urlpatterns = [
    path('assessment-create/', ExpertAssessmentCreateAPIView.as_view(), name='assessment-create'),
    path('list-company-province/', ExpertAssessmentCompanyProvinceListAPIView.as_view(), name='list-province'),
    path('list-company-district/<int:pk>/', ExpertAssessmentCompanyDistrictListAPIView.as_view(), name='list-district'),
    path('list-company/<int:pk>/', ExpertAssessmentCompanyListAPIView.as_view(), name='list-company'),
]
