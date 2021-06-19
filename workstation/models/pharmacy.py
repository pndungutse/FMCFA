from django.db import models
from workers.models.pharmacist import Pharmacist
from django import forms
from django.forms import ModelForm
from django.forms import Select, TextInput, Textarea


class Pharmacy(models.Model):
    name = models.CharField(max_length=100,blank=True, null=True)
    address = models.CharField(max_length=100,blank=True, null=True)
    agent = models.ForeignKey(Pharmacist, on_delete=models.CASCADE)



    def __str__(self):
        return self.name


    class Meta:
        db_table = "Pharmacy"

    
class PharmacyForm(forms.ModelForm):

    class Meta:
        model = Pharmacy
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': "Enter pharmacist"}),
            'address': TextInput(attrs={'class': 'form-control', 'placeholder': "Enter your Address"}),
            'agent': forms.Select(attrs={'class': 'h-form-control'}),
        }