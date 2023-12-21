"""
URL configuration for vendor_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import *

urlpatterns = [
    path('vendors/', VendorListCreateView.as_view(), name='vendor-list-create'),
    path('vendors/<int:pk>/', VendorDetailView.as_view(), name='vendor-detail'),
    path('vendors/<int:pk>/performance/', VendorPerformanceView.as_view(), name='vendor-performance'),
    path('purchase_orders/', PurchaseOrderListCreateView.as_view(), name='purchase-order-list-create'),
    path('purchase_orders/<int:pk>/', PurchaseOrderDetailView.as_view(), name='purchase-order-detail'),
    path('purchase_orders/<int:pk>/acknowledge/', PurchaseOrderAcknowledgeView.as_view(), name='purchase-order-acknowledge'),
]