from django import forms
from django.forms.widgets import TextInput,Textarea,Select,DateInput,CheckboxInput,FileInput

from . models import Profile

class SignInForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['email','password']

class SignUpForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['name','email','password']