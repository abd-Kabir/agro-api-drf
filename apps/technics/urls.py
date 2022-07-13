from django.urls import path
from apps.technics.views import (TechnicsCreateAPIView,
                                 TechnicsListAPIView,
                                 TechnicsUpdateAPIView,
                                 TechnicsDeleteAPIView,
                                 TechnicsDetailAPIView,
                                 TechnicsTypeInfoAPIView,
                                 TechnicsNameInfoAPIView,
                                 TechnicsNamePKInfoAPIView,
                                 TechnicsNameCreateAPIView,
                                 TechnicsTypeCreateAPIView,
                                 TechnicsCompanyList,
                                 TechnicsEditDataAPIView)

app_name = 'technics'
urlpatterns = [
    path('create/', TechnicsCreateAPIView.as_view(), name="create"),
    path('list/', TechnicsListAPIView.as_view(), name="list"),
    path('update/<int:pk>/', TechnicsUpdateAPIView.as_view(), name="update"),
    path('delete/<int:pk>/', TechnicsDeleteAPIView.as_view(), name="delete"),
    path('detail/<int:pk>/', TechnicsDetailAPIView.as_view(), name="details"),
    path('detail-edit/<int:pk>/', TechnicsEditDataAPIView.as_view(), name="edit_page_data"),
    path('types-info/', TechnicsTypeInfoAPIView.as_view(), name="technics_types"),
    path('types-info/create/', TechnicsTypeCreateAPIView.as_view(), name="technics_types_create"),
    path('names-info/', TechnicsNameInfoAPIView.as_view(), name="technics_names"),
    path('names-info/create/', TechnicsNameCreateAPIView.as_view(), name="technics_name_create"),
    path('names-info/<int:pk>/', TechnicsNamePKInfoAPIView.as_view(), name="technics_names_pk"),
    path('list-company/', TechnicsCompanyList.as_view(), name="list-company"),

]
