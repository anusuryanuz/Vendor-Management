from rest_framework import generics,filters,status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count, Avg, Sum, Case, When, Value
from django.db.models.functions import Coalesce
from django.utils import timezone
from .models import *
from .serializers import *
class VendorListCreateView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class VendorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class VendorPerformanceView(generics.RetrieveAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        vendor = self.get_object()
        vendor.update_metrics() 
        serializer = self.get_serializer(vendor)
        return Response(serializer.data)


    # def get(self, request, *args, **kwargs):
    #     vendor = self.get_object()
    #     data = {
    #         'on_time_delivery_rate': vendor.on_time_delivery_rate,
    #         'quality_rating_avg': vendor.quality_rating_avg,
    #         'average_response_time': vendor.average_response_time,
    #         'fulfillment_rate': vendor.fulfillment_rate,
    #     }
    #     return Response(data)

class PurchaseOrderListCreateView(generics.ListCreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['vendor__id', 'status']

    def get_queryset(self):
        return PurchaseOrder.objects.all()
class PurchaseOrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class PurchaseOrderAcknowledgeView(generics.UpdateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        
        serializer.save(acknowledgment_date=timezone.now(), status='Completed')
        instance.vendor.update_metrics()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)