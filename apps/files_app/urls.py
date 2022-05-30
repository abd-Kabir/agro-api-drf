from django.urls import path
from apps.files_app.views import DragDropCreateAPIView, DragDropDeleteAPIView, FileRetrieveAPIView

app_name = 'file'
urlpatterns = [
    path('drag-drop/', DragDropCreateAPIView.as_view(), name="drag_drop"),
    path('drag-drop-delete/<int:pk>/', DragDropDeleteAPIView.as_view(), name="drag_drop"),
    path('tech/<int:pk>/', FileRetrieveAPIView.as_view(), name="get_files_with_tech_id"),
]
