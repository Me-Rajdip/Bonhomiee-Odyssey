# from django.contrib import admin

# # Register your models here.
# from django.contrib import admin
# from .models import TravelRequest

# @admin.register(TravelRequest)
# class TravelRequestAdmin(admin.ModelAdmin):
#     list_display = ('name', 'destination', 'start_date', 'status')
#     list_filter = ('status', 'department')
#     search_fields = ('name', 'employee_number')

# admin.site.site_header = "Travel Request Administration"

from django.contrib import admin
from .models import TravelRequest

class TravelRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'destination', 'start_date', 'end_date', 'status', 'is_urgent', 'created_at')
    list_filter = ('status', 'is_urgent', 'flight_class', 'hotel_preference', 'user')
    search_fields = ('name', 'employee_number', 'destination', 'user__username')
    list_select_related = ('user',)
    actions = ['approve_requests', 'reject_requests']
    
    def approve_requests(self, request, queryset):
        queryset.update(status='approved', admin_verified=True)
        self.message_user(request, f"{queryset.count()} requests were approved.")
    approve_requests.short_description = "Approve selected requests"
    
    def reject_requests(self, request, queryset):
        queryset.update(status='rejected', admin_verified=True)
        self.message_user(request, f"{queryset.count()} requests were rejected.")
    reject_requests.short_description = "Reject selected requests"

admin.site.register(TravelRequest, TravelRequestAdmin)
