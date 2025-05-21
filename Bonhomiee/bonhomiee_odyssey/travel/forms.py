# travel/forms.py
from django import forms
from .models import TravelRequest
from django.contrib.auth.models import User
# travel/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'}),
        help_text='Required. Enter a valid email address.'
    )
    first_name = forms.CharField(required=True, max_length=30)
    last_name = forms.CharField(required=True, max_length=30)

    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if get_user_model().objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email


# class TravelRequestForm(forms.ModelForm):
#     class Meta:
#         model = TravelRequest
#         fields = ['employee_number', 'name', 'department', 'destination', 
#                  'travel_purpose', 'start_date', 'end_date', 
#                  'flight_class', 'hotel_preference', 'manager']
        
#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop('user', None)
#         super(TravelRequestForm, self).__init__(*args, **kwargs)
#         if user:
#             self.fields['manager'].queryset = User.objects.exclude(id=user.id)
#             # Automatically set the submitted_by field to the current user
#             self.instance.submitted_by = user

from django import forms
from .models import TravelRequest
from django.core.exceptions import ValidationError
from django.utils import timezone

class TravelRequestForm(forms.ModelForm):
    class Meta:
        model = TravelRequest
        fields = '__all__'
        exclude = ['user', 'status', 'created_at', 'updated_at', 'admin_verified', 'verification_notification_sent']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'travel_purpose': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date:
            if start_date > end_date:
                raise ValidationError("End date must be after start date")
            
            if start_date < timezone.now().date():
                raise ValidationError("Start date cannot be in the past")
        
        return cleaned_data