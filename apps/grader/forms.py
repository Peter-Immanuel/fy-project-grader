from django import forms
from .models import (
    Student,Staff
)
from django.utils.translation import ugettext_lazy as _




class StudentDetailsForm(forms.ModelForm):
    
    project_title = forms.CharField()
    supervisor = forms.ModelChoiceField(
        Staff.objects.filter(staff_type__in=["Supervisor", "Supervisor_and_Evaluator"], active=True))
    
    class Meta:
        model = Student
        exclude = ("active", "created_at", "updated_at", "id")
        
        
    def clean_email(self):
        email = self.cleaned_data.get("email")
        
        if "@st.futminna.edu.ng" not in email:
            raise forms.ValidationError(
                _("Please use your school email"))
        return email
    
    
    def create_record(self):
        title = self.cleaned_data.pop("project_title")
        supervisor = self.cleaned_data.pop("supervisor")
        student = self.model.objects.create_student_details(
            title=title,
            supervisor=supervisor,
            **self.cleaned_data
        )
        return student
        
    
        
