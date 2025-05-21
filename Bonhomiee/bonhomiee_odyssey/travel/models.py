from django.db import models
from django.contrib.auth.models import User

class TravelRequest(models.Model):
    FLIGHT_CLASS_CHOICES = [
        ('economy', 'Economy'),
        ('business', 'Business'),
        ('premium', 'Premium Economy'),
    ]
    
    HOTEL_CHOICES = [
        ('3star', '3 Star'),
        ('4star', '4 Star'),
        ('5star', '5 Star'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # This is the critical field
    employee_number = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    travel_purpose = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    flight_class = models.CharField(max_length=20, choices=FLIGHT_CLASS_CHOICES)
    hotel_preference = models.CharField(max_length=20, choices=HOTEL_CHOICES)
    notes = models.TextField(blank=True)
    is_urgent = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admin_verified = models.BooleanField(default=False)
    verification_notification_sent = models.BooleanField(default=False)
    
    @property
    def duration(self):
        return (self.end_date - self.start_date).days + 1
    
    def __str__(self):
        return f"TR-{self.id:04d} - {self.name} ({self.destination})"