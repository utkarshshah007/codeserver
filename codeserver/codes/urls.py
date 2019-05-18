from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('scan/', views.ScanTicketView.as_view(), name='scan-ticket'),
    path('api/scan/', views.ScanTicketAPIView.as_view(), name='api-scan')
]
