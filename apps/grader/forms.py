from typing import Any, Dict
from django import forms
from django.utils import timezone
import copy
from .models import (
    Student,Staff,
    ProjectProposalGrading,
    ProjectWorkProgress,
    InternalDefense,
    ExternalDefense,
    Project,
    ProductEvaluation
)
from django.utils.translation import ugettext_lazy as _
from apps.utils.constants import EVALUATION_TYPES
from django.db.models import Q
from apps.utils.security import validate_secret





class StudentRegistrationForm(forms.ModelForm):
    
    project_title = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)
    aims = forms.CharField(widget=forms.Textarea)
    objectives = forms.CharField(widget=forms.Textarea)
    supervisor = forms.ModelChoiceField(
        Staff.objects.filter(staff_type__in=["Supervisor_and_Evaluator"], active=True))
    
    class Meta:
        model = Student
        exclude = ("active", "created_at", "updated_at", "id")
        
        
    def clean_email(self):
        email = self.cleaned_data.get("email")
        
        if "@st.futminna.edu.ng" not in email:
            raise forms.ValidationError(
                _("Please use your school email"))
        return email
    
    def clean_matric_number(self):
        matric_number = self.cleaned_data.get("matric_number")
        
        try:
            Student.objects.get(matric_number=matric_number.lower())
            raise forms.ValidationError(
                _("Student with matric number already exists! who are you?")
            )
        except Student.DoesNotExist:
            pass
        
        return matric_number
    
    
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
  
  
class StudentSearchForm(forms.Form):
    
    student = forms.CharField()
    
    def search(self):
        student = self.cleaned_data.get("student").lower()
        result = Student.objects.filter(
            Q(email=student) | Q(matric_number=student), graduated=False)

        if result.exists():
            return result.first(), True
        return None, False
  

class StudentProjectEditForm(forms.ModelForm):
    
    class Meta:
        model = Project
        fields = (
            "title", "aims", "objectives", "description", 
        )
        
    def update(self, project):
        updatd_project = project.update_records(self.cleaned_data)
        return updatd_project
        



# Staff Forms   
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
    
    # def clean_signature(self):
    #     signature = self.cleaned_data.get("signature", None)
    #     if signature.size > 50000:
    #         raise forms.ValidationError(
    #             _("Signature should be at most 50kb"))
    #     return signature
    
    def create_record(self):
        
        self.cleaned_data["email"] = self.cleaned_data.pop("email").lower()
        staff = self.Meta.model.objects.create_staff_profile(
            password=self.cleaned_data.pop("password"),
            **self.cleaned_data
        )
        
        return staff
  
  
  
# Evaluation forms 
class StudentEvaluationSearchForm(forms.Form):
    
    student = forms.CharField()
    type =  forms.ChoiceField(choices=EVALUATION_TYPES.items())
    
    def search(self):
        student = self.cleaned_data.get("student").lower()
        result = Student.objects.filter(
            Q(email=student) | Q(matric_number=student), graduated=False)

        if result.exists():
            return result.first(), True
        return None, False
    
    def can_evaluate_student(self, student, staff):
        eval_type = self.cleaned_data.get("type")
        
        # check cordinator approval
        
        if not student.project.cordinator_approval:
            return "Sorry, Student topic hasn't been approved by Cordinator.", False
        
        if student.project.supervisor == staff:
            return "Sorry, you can't evaluate your project student.", False
        
        if eval_type == "proposal":
            if ProjectProposalGrading.objects.filter(evaluator=staff, student=student).exists():
                return "Sorry, you have evaluated this student", False
            
            if ProjectProposalGrading.objects.filter(student=student).count() >= 3:
                return "Sorry, Maximum Evaluation reached.", False
            
        elif eval_type == "work_progress":
            if ProjectWorkProgress.objects.filter(evaluator=staff, student=student).exists():
                return "Sorry, you have evaluated this student", False
            
            if ProjectWorkProgress.objects.filter(student=student).count() >= 3:
                return "Sorry, Maximum Evaluation reached.", False     
            
        elif eval_type == "internal_defence":
            if InternalDefense.objects.filter(evaluator=staff, student=student).exists():
                return "Sorry, you have evaluated this student", False
            
            if InternalDefense.objects.filter(student=student).count() >= 3:
                return "Sorry, Maximum Evaluation reached.", False     
            
        elif eval_type == "external_defence":
            if ExternalDefense.objects.filter(evaluator=staff, student=student).exists():
                return "Sorry, you have evaluated this student", False
            
            if ExternalDefense.objects.filter(student=student).count() >= 1: 
                return "Sorry, Maximum Evaluation reached.", False

        return "", True
    
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
    
    def validate_evaluator(self, staff_profile):
        return validate_secret(self.cleaned_data.get("secret"), staff_profile.secret)
    
    def can_evaluate(self, student, staff_profile):
        evaluation = self.Meta.model.objects.filter(
            session=student.session,
            faculty=student.faculty,
            department=student.department,
            student=student,
            project=student.project,
            evaluator=staff_profile,
        )
        
        if len(evaluation) >= 1:
            return False
        return True
    
    def evaluate(self, student, staff):
        total = (
            self.cleaned_data.get("objective_scope") + self.cleaned_data.get("research_methodology") +
            self.cleaned_data.get("literature_review") + self.cleaned_data.get("communication_skills")
        )
        
        self.Meta.model.objects.create(
            session=student.session,
            faculty=student.faculty,
            department=student.department,
            student=student,
            project=student.project,
            objective_scope =self.cleaned_data.get("objective_scope"),
            research_methodology=self.cleaned_data.get("research_methodology"),
            literature_review=self.cleaned_data.get("literature_review"),
            communication_skills=self.cleaned_data.get("communication_skills"),
            total=total,
            comment = self.cleaned_data.get("comment"),
            evaluator=staff,
            date_evaluated=timezone.now().date(),
            signed=True
        )
        return


class WorkProgressEvaluationForm(forms.ModelForm):
    
    secret = forms.CharField()
    
    class Meta:
        model = ProjectWorkProgress
        fields = (
            "project_methodology",
            "preliminary_result", "communication_skills",
            "comment", "secret"
        )
        
    def clean(self):
        score_hashmap = {
            "score_20" : ["communication_skills"],
            "score_40" : ["project_methodology", "preliminary_result"],
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
                elif key in score_hashmap["score_40"]:
                    if value < 0 or value > 40:
                        self.add_error(key, "Score should be between 0 - 40")
                        
        if self.errors:
            raise forms.ValidationError("Error please check again")
        return self.cleaned_data
    
    def validate_evaluator(self, staff_profile):
        return validate_secret(self.cleaned_data.get("secret"), staff_profile.secret)
    
    def can_evaluate(self, student, staff_profile):
        evaluation = self.Meta.model.objects.filter(
            session=student.session,
            faculty=student.faculty,
            department=student.department,
            student=student,
            project=student.project,
            evaluator=staff_profile,
        )
        
        if len(evaluation) >= 1:
            return False
        return True
    
    def evaluate(self, student, staff):
        total = (
            self.cleaned_data.get("project_methodology") + self.cleaned_data.get("preliminary_result")
            + self.cleaned_data.get("communication_skills")
        )
        
        self.Meta.model.objects.create(
            session=student.session,
            faculty=student.faculty,
            department=student.department,
            student=student,
            project=student.project,
            project_methodology=self.cleaned_data.get("project_methodology"),
            preliminary_result=self.cleaned_data.get("preliminary_result"),
            communication_skills=self.cleaned_data.get("communication_skills"),
            total=total,
            comment = self.cleaned_data.get("comment"),
            evaluator=staff,
            date_evaluated=timezone.now().date(),
            signed=True
        )
        return
    
        
class DefenseEvaluationForm(forms.Form):
    
    problem_statement = forms.IntegerField()
    project_methodology = forms.IntegerField()
    result_discussion = forms.IntegerField()
    conclusion = forms.IntegerField()
    communication_skills = forms.IntegerField()
    # device_score = forms.IntegerField(required=False)
    comment = forms.CharField(widget=forms.Textarea)
    secret = forms.CharField()
    
    def clean(self):
        score_hashmap = {
            "score_5" : ["conclusion", "communication_skills"],
            "score_10" : [
                "problem_statement", "project_methodology",
                "result_discussion", "device_score"
            ],
            "skips" : ["comment", "secret"]
        }
        
        data = copy.deepcopy(self.cleaned_data)
        for key, value in data.items():
            if key in score_hashmap["skips"]:
                continue
            else:
                if key in score_hashmap["score_5"]:
                    if value < 0 or value > 5:
                        self.add_error(key, "Score should be between 0 - 5")
                        
                elif key in score_hashmap["score_10"]:
                    if value < 0 or value > 10:
                        self.add_error(key, "Score should be between 0 - 10")
                        
                        
        if self.errors:
            raise forms.ValidationError("Error please check again")
        return self.cleaned_data
    
    def clean_external(self):
        score_hashmap = {
            "score_5" : ["conclusion", "communication_skills"],
            "score_10" : ["problem_statement"],
            "skips" : ["comment", "secret", "internal"]
        }
        
        data = copy.deepcopy(self.cleaned_data)
        for key, value in data.items():
            if key in score_hashmap["skips"]:
                continue
            else:
                if key in score_hashmap["score_5"]:
                    if value < 0 or value > 5:
                        self.add_error(key, "Score should be between 0 - 5")
                        
                elif key in score_hashmap["score_10"]:
                    if value < 0 or value > 10:
                        self.add_error(key, "Score should be between 0 - 10")
                        
        if self.errors:
            raise forms.ValidationError("Error please check again")
        return self.cleaned_data
    
    def validate_evaluator(self, staff_profile):
        return validate_secret(self.cleaned_data.get("secret"), staff_profile.secret)
    
    def can_evaluate(self, student, staff_profile):
        
        evaluation = InternalDefense.objects.filter(
            session=student.session,
            faculty=student.faculty,
            department=student.department,
            student=student,
            project=student.project,
            evaluator=staff_profile,
        )
                
        if len(evaluation) >= 1:
            return False
        return True
    
    def evaluate(self, student, staff):
        
        total = (
            (self.cleaned_data.get("problem_statement") * 2)  + 
            (self.cleaned_data.get("project_methodology") * 3) + 
            (self.cleaned_data.get("result_discussion") * 3) + 
            (self.cleaned_data.get("conclusion") * 2) + 
            (self.cleaned_data.get("communication_skills") * 2)
        )
        
        InternalDefense.objects.create(
            session=student.session,
            faculty=student.faculty,
            department=student.department,
            student=student,
            project=student.project,
            problem_statement=(self.cleaned_data.get("problem_statement") * 2),
            project_methodology=(self.cleaned_data.get("project_methodology") * 3),
            result_discussion=(self.cleaned_data.get("result_discussion") * 3),
            conclusion=(self.cleaned_data.get("conclusion") * 2),
            communication_skills=(self.cleaned_data.get("communication_skills") * 2),
            # device_score=(self.cleaned_data.get("device_score", ) * 2),
            total=total,
            comment = self.cleaned_data.get("comment"),
            evaluator=staff,
            date_evaluated=timezone.now().date(),
            signed=True
        )
        return
    
          
class ExternalDefenseEvaluationForm(DefenseEvaluationForm):
    
    def can_evaluate(self, student):
            
        evaluations = ExternalDefense.objects.filter(
            session=student.session,
            faculty=student.faculty,
            department=student.department,
            student=student,
            project=student.project,
        )
                
        if len(evaluations) >= 1:
            return False
        return True
    
    def evaluate(self, student, staff):
            
        total = (
            (self.cleaned_data.get("problem_statement") * 2)  + 
            (self.cleaned_data.get("project_methodology") * 3) + 
            (self.cleaned_data.get("result_discussion") * 3) + 
            (self.cleaned_data.get("conclusion") * 2) + 
            (self.cleaned_data.get("communication_skills") * 2)
        )
        
        ExternalDefense.objects.create(
            session=student.session,
            faculty=student.faculty,
            department=student.department,
            student=student,
            project=student.project,
            problem_statement=(self.cleaned_data.get("problem_statement") * 2),
            project_methodology=(self.cleaned_data.get("project_methodology") * 3),
            result_discussion=(self.cleaned_data.get("result_discussion") * 3),
            conclusion=(self.cleaned_data.get("conclusion") * 2),
            communication_skills=(self.cleaned_data.get("communication_skills") * 2),
            total=total,
            comment = self.cleaned_data.get("comment"),
            evaluator=staff,
            date_evaluated=timezone.now().date(),
            signed=True
        )
        return
        

class ProductEvaluationForm(forms.ModelForm):
    secret = forms.CharField()
    
    class Meta:
        model = ProductEvaluation
        fields = (
            "hardware", "software", 
            "packaging","functionality",
            "simulation", "comment", "secret"
        )
    
    
    def clean(self):
        score_hashmap = {
            "score_20" : ["hardware_score", "software_score", "packaging","functionality","simulation"],
        }
        data = copy.deepcopy(self.cleaned_data)
        for key, value in data.items():
            if key in score_hashmap["score_20"]:
                if value < 0 or value > 20:
                    self.add_error(key, "Score should be between 0 - 20")
                        
        if self.errors:
            raise forms.ValidationError("Error please check again")
        return self.cleaned_data
    
    def validate_evaluator(self, staff_profile):
        return validate_secret(self.cleaned_data.get("secret"), staff_profile.secret)
    
    def can_evaluate(self, student, staff_profile):
        evaluation = self.Meta.model.objects.filter(
            session=student.session,
            faculty=student.faculty,
            student=student,
            department=student.department,
            project=student.project,
            evaluator=staff_profile,
        )
        
        if len(evaluation) >= 3:
            return False
        return True
    
    def evaluate(self, student, staff):
        total = (
            self.cleaned_data.get("hardware") + self.cleaned_data.get("software")
            + self.cleaned_data.get("packaging") + self.cleaned_data.get("functionality")
            + self.cleaned_data.get("simulation")
        )
        
        self.Meta.model.objects.create(
            session=student.session,
            faculty=student.faculty,
            department=student.department,
            project=student.project,
            student=student,
            
            hardware=self.cleaned_data.get("hardware"),
            software=self.cleaned_data.get("software"),
            packaging=self.cleaned_data.get("packaging"),
            functionality=self.cleaned_data.get("functionality"),
            simulation=self.cleaned_data.get("simulation"),
            
            total=total,
            
            
            evaluator=staff,
            comment = self.cleaned_data.get("comment"),
            date_evaluated=timezone.now().date(),
            signed=True
        )
        return
    
    
    
class ProjectApprovalForm(forms.Form):
    
    comment = forms.CharField(widget=forms.Textarea)
    secret = forms.CharField()
    approval = forms.BooleanField(required=False)
    
    def perform_approval(self, project, staff):
        
        if project.supervisor == staff and staff.user.is_superuser:
            project.approve_cordinator_student(
                self.cleaned_data.get("approval"),
                self.cleaned_data.get("comment")
            )
        else:    
            if project.supervisor == staff:
                project.approve_by_supervisor(
                    self.cleaned_data.get("approval"),
                    self.cleaned_data.get("comment")
                )
            else:
                project.approve_by_cordinator(
                    self.cleaned_data.get("approval"),
                    self.cleaned_data.get("comment")
                )
            

        
    
    def validate_evaluator(self, staff_profile):
        return validate_secret(self.cleaned_data.get("secret"), staff_profile.secret)
 
    
    
    

class ChangeTableForm(forms.Form):
    choices = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)
    
     
     
class ProjectUpdateForm(forms.ModelForm):
    pass 
