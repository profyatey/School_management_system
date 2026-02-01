from django import forms
from .models import Teacher

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ["name", "email", "phone", "school", "subject"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "school": forms.Select(attrs={"class": "form-select"}),
            "subject": forms.Select(attrs={"class": "form-select"}),
        }
