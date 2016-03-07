from monitoring_app.models import UserProfile,Machine
from django.contrib.auth.models import User 
from django import forms
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class MachineForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
	
    class Meta:
        model = Machine
        fields = ('name', 'address', 'username','password')