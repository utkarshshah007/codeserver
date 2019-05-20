from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('ticket/add/', views.CreateTicketsView.as_view(), name='create-tickets'),
    path('scan/', views.ScanTicketView.as_view(), name='scan-ticket'),
    path('api/', views.DocView.as_view(), name='docs'),
    path('api/scan/', views.ScanTicketAPIView.as_view(), name='api-scan')
]
