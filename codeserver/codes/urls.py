from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('scan/', views.ScanTicketView.as_view(), name='scan-ticket'),
    path('scan/<code>/', views.ScanTicketView.as_view(), name='scanned-ticket-info')
]
