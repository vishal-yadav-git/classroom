from django import forms
from django.contrib.auth import get_user_model
import re
from django.core.exceptions import ValidationError


User = get_user_model()

class StudentRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=False)
    phone = forms.CharField(max_length=15, required=True)

    course_choices = [
        ('ca_final', 'CA Final'),
        ('cma_final', 'CMA Final'),
        ('ca_inter', 'CA Inter'),
        ('cma_inter', 'CMA Inter'),
        ('cs', 'CS'),
        ('tenth', '10th'),
        ('twelfth', '12th'),
        ('other', 'Other'),
    ]
    course = forms.ChoiceField(choices=course_choices, required=True)

    occupation_choices = [
        ('faculty', 'Faculty'),
        ('student', 'Student'),
        ('other', 'Other'),
    ]
    occupation = forms.ChoiceField(choices=occupation_choices, required=True)

    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'phone',
            'email',
            'course',
            'occupation',
            'password'
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already taken. Please use a different email.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")

        return cleaned_data
    

# classroom/forms.py
class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'Enter your email'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Enter password'
    }))

