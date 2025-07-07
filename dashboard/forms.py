from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'w-full px-4 py-2 border rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-400',
        'placeholder': 'Email'
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {
            'username': None,
            'password1': None,
            'password2': None,
        }
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-400',
                'placeholder': 'Username'
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-400',
                'placeholder': 'Password'
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-400',
                'placeholder': 'Confirm Password'
            }),
        }


class TweetForm(forms.Form):
    tweet = forms.CharField(
        max_length=280,
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Whats happening?'}),
        label='Post a Tweet'
    )
