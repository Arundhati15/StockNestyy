from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Stock

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['symbol', 'nickname']
        widgets = {
            'symbol': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'AAPL / RELIANCE.NS / TSLA'}),
            'nickname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional name'}),
        }

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in ['username','password1','password2']:
            self.fields[f].widget.attrs.update({'class':'form-control'})
