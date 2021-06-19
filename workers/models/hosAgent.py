from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.forms import Select, TextInput, Textarea

class HospitalAgent(models.Model):
    user = models.OneToOneField(User,null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    age = models.IntegerField(blank=True, null=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    dob = models.DateTimeField(blank=True, null=True)
    phone =  models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return self.name
    

    class Meta:
        db_table = "HospitalAgent"


class HospitalAgentForm(forms.ModelForm):

    class Meta:
        model = HospitalAgent
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': "Enter hospital Agent"}),
            'address': TextInput(attrs={'class': 'form-control', 'placeholder': "Enter your Address"}),
            'phone': TextInput(attrs={'class': 'form-control', 'placeholder': "Enter your phone"}),
            'email': TextInput(attrs={'class': 'form-control', 'placeholder': "Enter your email"}),
            'dob': TextInput(attrs={'class': 'form-control', 'type':'date'}),
        }
        
class HospitalAgentRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2'
        )
        
    def __init__(self, *args, **kwargs):
        super(HospitalAgentRegistrationForm, self).__init__(*args, **kwargs)
        
        for fieldname in ['username','email','password1','password2']:
            self.fields[fieldname].help_text = None
    def save(self, commit=True):
        user = super(HospitalAgentRegistrationForm,self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            
        return user