from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import CustomUser, Booking, Review, TourPackage
from django.contrib.auth import get_user_model
# from django.contrib.auth.models import User
# ✅ Custom User Registration Form
User = get_user_model()
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text="Your password must contain at least 8 characters."
    )
    
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'phone_number', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = "Minimum 8 characters with at least one uppercase, lowercase, and number"
        self.fields['password2'].label = "Confirm Password"

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if CustomUser.objects.filter(email__iexact=email).exists():
            raise ValidationError("This email is already registered.")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number').strip()
        if CustomUser.objects.filter(phone_number__iexact=phone_number).exists():
            raise ValidationError("This phone number is already registered.")
        return phone_number

def save(self, commit=True):
    user = super().save(commit=False)
    user.username = self.cleaned_data['email'].split('@')[0]  # Auto-generate username from email
    user.user_type = 'C'  # Default to Customer
    user.email = self.cleaned_data['email'].lower()
    user.phone_number = self.cleaned_data['phone_number'].strip()
    user.email_verified = True
    if commit:
        user.save()
        #self.save_m2m()  # Save many-to-many relationships
    return user

# ✅ Booking Form
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['tour_package', 'travelers', 'start_date', 'end_date', 'special_requests', 'passengers']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'special_requests': forms.Textarea(attrs={'rows': 4}),
            'tour_package': forms.Select(attrs={'class': 'form-control'}),
            'travelers': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['tour_package'].queryset = TourPackage.objects.all()


# ✅ Review Form
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
        }


# ✅ Login Form
class LoginForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        max_length=254,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'})
    )


# ✅ Tour Package Form
class TourPackageForm(forms.ModelForm):
    title = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'maxlength': 255, 'placeholder': 'Enter tour package title'})
    )

    class Meta:
        model = TourPackage
        fields = ['title']
