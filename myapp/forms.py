from django import forms
from .models import Company, Manager, Employee

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'
        widgets = {
            'password': forms.PasswordInput(),
        }

class ManagerForm(forms.ModelForm):
    class Meta:
        model = Manager
        fields = '__all__'
        widgets = {
            'password': forms.PasswordInput(),
        }

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        widgets = {
            'password': forms.PasswordInput(),
        }
