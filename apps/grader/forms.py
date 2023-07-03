from django import forms
from .models import (
    Student,Staff
)
from django.utils.translation import ugettext_lazy as _
from apps.utils.constants import EVALUATION_TYPES
from django.db.models import Q





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
        
        # Make matric number and email lower case for easy search
        self.cleaned_data["email"] = self.cleaned_data.pop("email").lower()
        self.cleaned_data["matric_number"] = self.cleaned_data.pop("matric_number").lower()
        
        
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
    
        if "@futminna.edu.ng" not in email:
            raise forms.ValidationError(
                _("Please use your school email"))
        return email
    
    def create_record(self):
        
        self.cleaned_data["email"] = self.cleaned_data.pop("email").lower()
        staff = self.Meta.model.objects.create_staff_profile(
            password=self.cleaned_data.pop("password"),
            **self.cleaned_data
        )
        
        return staff
  
  
class StudentEvaluationSearchForm(forms.Form):
    
    student = forms.CharField()
    type =  forms.ChoiceField(choices=EVALUATION_TYPES.items())
    
    def search(self):
        student = self.cleaned_data.get("student")
        result = Student.objects.filter(
            Q(email=student) | Q(matric_number=student), graduated=False)

        if result.exists():
            return result.first(), True
        return None, False
    
    
    
    
        
