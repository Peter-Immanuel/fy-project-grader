from django import forms
from .models import (
    Student,Staff
)
from django.utils.translation import ugettext_lazy as _




class StudentRegistrationForm(forms.ModelForm):
    
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
        student = self.Meta.model.objects.create_student_details(
            title=title,
            supervisor=supervisor,
            **self.cleaned_data
        )
        return student
    
    
class StaffRegistrationForm(forms.ModelForm):
    
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
        required=True
    )

    
    class Meta:
        model = Staff
        exclude = ("user", "active", "id")
        
        
    def clean_email(self):
        email = self.cleaned_data.get("email")
    
        if "@st.futminna.edu.ng" not in email:
            raise forms.ValidationError(
                _("Please use your school email"))
        return email
    
    def create_record(self):
        
        staff = self.Meta.model.objects.create_staff_profile(
            password=self.cleaned_data.pop("password"),
            **self.cleaned_data
        )
        
        return staff
    
        
