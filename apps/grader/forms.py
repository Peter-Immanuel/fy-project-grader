from django import forms
import copy
from .models import (
    Student,Staff,
    ProjectProposalGrading,
    ProjectWorkProgress,
    InternalDefense,
    ExternalDefense
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
    
    

class ProposalEvaluationForm(forms.ModelForm):
    
    secret = forms.CharField()
    
    class Meta:
        model = ProjectProposalGrading
        fields = (
            "objective_scope", "research_methodology",
            "literature_review", "communication_skills",
            "comment", "secret"
        )
        
    def clean(self):
        score_hashmap = {
            "score_20" : ["objective_scope", "communication_skills"],
            "score_30" : ["research_methodology", "literature_review"],
            "skips" : ["comment", "secret"]
        }
        data = copy.deepcopy(self.cleaned_data)
        for key, value in data.items():
            if key in score_hashmap["skips"]:
                continue
            else:
                if key in score_hashmap["score_20"]:
                    if value < 0 or value > 20:
                        self.add_error(key, "Score should be between 0 - 20")
                        # forms.ValidationError("Score should be between 0 - 20")
                elif key in score_hashmap["score_30"]:
                    if value < 0 or value > 30:
                        self.add_error(key, "Score should be between 0 - 30")
                        # forms.ValidationError("Score should be between 0 - 30")
                        
        if self.errors:
            raise forms.ValidationError("Error please check again")
        return self.cleaned_data
    
        

class WorkProgressEvaluationForm(forms.ModelForm):
    
    secret = forms.CharField()
    
    class Meta:
        model = ProjectWorkProgress
        fields = ("comment", )
        
        
class DefenseEvaluationForm(forms.ModelForm):
    
    secret = forms.CharField()
    internal = forms.BooleanField(required=False)
    
    class Meta:
        model = InternalDefense
        fields = ("comment", )
        
    
    
        
