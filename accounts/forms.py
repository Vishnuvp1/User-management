from django import forms

from django.contrib.auth.models import User




class UserUpdate(forms.ModelForm):
    username = forms.CharField(required=True, max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Enter your Username'}))
    


    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username',  'email'] 
