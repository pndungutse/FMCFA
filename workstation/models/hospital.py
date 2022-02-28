from django.db import models
from django.db.models.fields import FloatField
from workers.models.hosAgent import HospitalAgent
from django import forms
from django.forms import ModelForm
from django.forms import Select, TextInput, Textarea
from beneficiary.models import Beneficiary
from workstation.models.pharmacy import Pharmacy


STATUS = [
    ("PENDING", "PENDING"),
    ("DELIVERED", "DELIVERED"),
]

class Drug(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    unitPrice = models.FloatField()
    sickness = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return self.name
    

class DrugForm(forms.ModelForm):
    
    class Meta:
        model = Drug
        fields = '__all__'
        


class Hospital(models.Model):
    name = models.CharField(max_length=100,blank=True, null=True)
    address = models.CharField(max_length=100,blank=True, null=True)
    agent = models.ForeignKey(HospitalAgent, on_delete=models.CASCADE)


    def __str__(self):
        return self.name


    class Meta:
        db_table = "Hospital"
        
class Pass(models.Model):
    hospital = models.ForeignKey(Hospital,null=True, on_delete=models.CASCADE)
    beneficiary = models.ForeignKey(Beneficiary, null=True, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False)

    
    def __str__(self):
        return '%s - %s - %s' %(self.hospital.name, self.beneficiary.name , self.date_created) 

class Exam(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    price = models.FloatField() 
    
    def __str__(self):
        return self.name
    
class ExamForm(forms.ModelForm):
    
    class Meta:
        model = Exam
        fields = '__all__'


class Medical_Exam(models.Model):
    beneficiary = models.ForeignKey(Beneficiary, null=True, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, null=True, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, null=True, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return '%s - %s - %s' %(self.beneficiary.name , self.exam.name, self.hospital.name) 

class Ordonance(models.Model):
    beneficiary = models.ForeignKey(Beneficiary, null=True, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital,null=True, on_delete=models.CASCADE)
    drug = models.ForeignKey(Drug, null=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS, default='PENDING')
    # pharmacy = models.ForeignKey(Pharmacy, null=True, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return '%s - %s - %s' %(self.beneficiary.name, self.drug.name , self.date_created)
    
class OrdonanceForm(forms.ModelForm):
    class Meta:
        model = Ordonance
        fields = ('drug',)
        labels = {
            'drug':'Drug'
        }

class HospitalForm(forms.ModelForm):

    class Meta:
        model = Hospital
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': "Enter Hospital Name"}),
            'address': TextInput(attrs={'class': 'form-control', 'placeholder': "Enter your Address"}),
            'agent': forms.Select(attrs={'class': 'h-form-control'}),
        }
        
class Medical_ExamForm(forms.ModelForm):
    class Meta:
        model = Medical_Exam
        fields = ('exam',)
        labels = {
            'exam':'Exam',
            
        }
    
class DrugsIssuing(models.Model):
    pharmacy = models.ForeignKey(Pharmacy, null=True, on_delete=models.CASCADE)
    beneficiary = models.ForeignKey(Beneficiary, null=True, on_delete=models.CASCADE)
    drug = models.ForeignKey(Drug, null=True, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    totalPrice = models.FloatField()
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return '%s - %s - %s - %s' %(self.pharmacy.name, self.beneficiary.name , self.drug.name, self.date_created)

    
    # def save(self, *args, **kwargs):
    #     totalPrice = self.quantity * self.drug.unitPrice

    #     self.totalPrice = totalPrice
    #     super(DrugsIssuing, self).save(*args, **kwargs)
    
class DrugsIssuingForm(forms.ModelForm):
    class Meta:
        model = DrugsIssuing
        fields = ('beneficiary', 'drug', 'quantity')
        labels = {
            'beneficiary': 'Beneficiary',
            'drug': 'Drug',
            'quantity': 'Quantity',
        }

class Suggestion(models.Model):
    hospital = models.ForeignKey(Hospital,null=True, on_delete=models.CASCADE)
    beneficiary = models.ForeignKey(Beneficiary, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True, max_length=255)
    suggestion = models.TextField(null=True, blank=True, max_length=255)
    
    def __str__(self):
        return self.title
    
class SuggestionForm(forms.ModelForm):
    class Meta:
        model = Suggestion
        fields = ('title', 'description', 'suggestion')
        widgets = {
            'title': TextInput(attrs={'class': 'form-control', 'placeholder': "Enter Suggestion Title"}),
            'description': Textarea(attrs={'class': 'form-control', 'placeholder': "Enter Suggestion Description"}),
            'suggestion': Textarea(attrs={'class': 'form-control', 'placeholder': "Enter Suggestion"}),


        }
        labels = {
            'title': 'Title',
            'description': 'Description',
            'suggestion': 'Suggestion'
        }
        
    

