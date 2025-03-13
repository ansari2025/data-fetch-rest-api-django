from django.urls import path
from .views import UploadCSVView, AppointmentListView

urlpatterns = [
    path('upload-csv/', UploadCSVView.as_view(), name='upload_csv'),
    path('appointments/', AppointmentListView.as_view(), name='appointments'),
]
