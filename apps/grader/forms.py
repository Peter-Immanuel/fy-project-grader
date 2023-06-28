from django import forms
from .models import (
    Student,
)
from django.utils.translation import ugettext_lazy as _




class StudentDetailsForm(forms.ModelForm):
    
    class Meta:
        model = Student
        exclude = ("active", "created_at", "updated_at", "id")
        
        
    def clean_email(self):
        email = self.cleaned_data.get("email")
        
        if "@st.futminna.edu.ng" not in email:
            raise forms.ValidationError(
                _("Please use your school email"))
        return email
    
        
