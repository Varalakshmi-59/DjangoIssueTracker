from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                'class': 'appearance-none rounded-none relative block w-full px-3 py-2 border '
                        'border-gray-300 placeholder-gray-500 text-gray-900 '
                        'focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm',
                'placeholder': 'Email',
            }
        )
    )
    
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'appearance-none rounded-none relative block w-full px-3 py-2 border '
                        'border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md '
                        'focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm',
                'placeholder': 'Username',
            }
        )
    )
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'appearance-none rounded-none relative block w-full px-3 py-2 border '
                        'border-gray-300 placeholder-gray-500 text-gray-900 '
                        'focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm',
                'placeholder': 'Password',
            }
        )
    )
    
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'appearance-none rounded-none relative block w-full px-3 py-2 border '
                        'border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md '
                        'focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm',
                'placeholder': 'Confirm Password',
            }
        )
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "The two password fields must match.")
        
        return cleaned_data


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'bio', 'profile_picture')
        
