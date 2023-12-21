from django.db import models
from django.utils import timezone
from datetime import timedelta

class Vendor(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=20, unique=True)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)

    def __str__(self):
        return self.name
    
    

    def calculate_on_time_delivery_rate(self):
        completed_pos = self.purchaseorder_set.filter(status='completed', delivery_date__isnull=False)
        on_time_deliveries = completed_pos.filter(delivery_date__lte=timezone.now())
        return (on_time_deliveries.count() / completed_pos.count()) * 100 if completed_pos.count() > 0 else 0

    def calculate_quality_rating_avg(self):
        completed_pos = self.purchaseorder_set.filter(status='completed', quality_rating__isnull=False)
        total_quality_ratings = completed_pos.exclude(quality_rating__isnull=True).count()
        if total_quality_ratings > 0:
            return completed_pos.aggregate(avg_rating=Coalesce(Avg('quality_rating'), 0))['avg_rating']
        return 0
       
    def calculate_average_response_time(self):
        acknowledged_pos = self.purchaseorder_set.filter(acknowledgment_date__isnull=False, issue_date__isnull=False)
        response_times = [
            (po.acknowledgment_date - po.issue_date).total_seconds()
            for po in acknowledged_pos
            if po.issue_date and po.acknowledgment_date  # Check for None values
        ]

        return sum(response_times) / len(response_times) if len(response_times) > 0 else 0


    
    def calculate_fulfillment_rate(self):
        completed_pos = self.purchaseorder_set.filter(status='completed')
        successful_fulfillments = completed_pos.filter(issue_date__isnull=False, acknowledgment_date__isnull=False)
        return (successful_fulfillments.count() / completed_pos.count()) * 100 if completed_pos.count() > 0 else 0

    def update_metrics(self):
        self.on_time_delivery_rate = self.calculate_on_time_delivery_rate()
        self.quality_rating_avg = self.calculate_quality_rating_avg()
        self.average_response_time = self.calculate_average_response_time()
        self.fulfillment_rate = self.calculate_fulfillment_rate()
        self.save()
    

class PurchaseOrder(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    po_number = models.CharField(max_length=255, unique=True)
    order_date = models.DateTimeField(default=timezone.now)
    delivery_date = models.DateTimeField(null=True, blank=True)
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=20, default='pending')
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField(null=True, blank=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    # Override the save method to update vendor metrics
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.status == 'Completed':
            self.vendor.update_metrics()

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()