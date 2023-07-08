from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import (
    StudentRegistrationForm,
    StaffRegistrationForm,
    StudentEvaluationSearchForm,
    ProposalEvaluationForm,
    WorkProgressEvaluationForm,
    DefenseEvaluationForm,
)
from .models import Student
from apps.utils.utils import query_params
from django.views import View
from django.http import HttpResponse
from apps.utils.constants import EVALUATION_TYPES





class StudentRegistrationView(View):
    
    form = StudentRegistrationForm
    template="components/students/student_form.html"
    success_template="components/success-dialog.html"
    
    def get(self, request, *args, **kwargs):
        form = self.form()
        return render(request, self.template, {"form":form})
    
    def post(self, request, *args, **kwargs):
        form = self.form(data=request.POST)
        if form.is_valid():
            form.create_record()
            context = {
                "message": "Thank you for updating your record"
            }
            return render(request, self.success_template, context)
        else:
            return render(request, self.template, {"form":form})

            
class StaffRegistrationView(View):
    
    form = StaffRegistrationForm
    template = "components/staffs/staff_registration_form.html"
    # template = "demo.html"
    success_template="components/success-dialog.html"
    
    def get(self, request, *args, **kwargs):
        form = self.form()
        return render(request, self.template, {"form":form})
    
    def post(self, request, *args, **kwargs):
        form = self.form(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.create_record()
            context = {
                "message": "Thank you for creating your record"
            }
            return render(request, self.success_template, context)
        
        else:
            return render(request, self.template, {"form":form})


class StudentEvaluationSearchView(View):
    
    form = StudentEvaluationSearchForm
    template = "components/search_form.html"
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:    
            form = self.form()
            return render(request, self.template, {"form":form})
        return redirect("authenticator:evaluator-login")
    
    def post(self, request, *args, **kwargs):
        form = self.form(data=request.POST)
        if form.is_valid():
            student, found = form.search()
            evaluation = form.cleaned_data.get("type")
            if found:

                if EVALUATION_TYPES[evaluation] == EVALUATION_TYPES["proposal"]:
                    return redirect("grader:proposal-evaluation", student.id)
                
                elif EVALUATION_TYPES[evaluation] == EVALUATION_TYPES["work_progress"]:
                    return redirect("grader:work-progress-evaluation", student.id)
                
                elif EVALUATION_TYPES[evaluation] == EVALUATION_TYPES["internal_defence"]:
                    return redirect(reverse("grader:internal-defense-evaluation", args=[student.id]))
                
                elif EVALUATION_TYPES[evaluation] == EVALUATION_TYPES["external_defence"]:
                    pass
                
                
            else:
                form.add_error("student", "Not Found!")
                context = {
                    "message":"Sorry, Student not found.",
                    "form":form
                }
                return render(request, self.template, context)
        
        else:
            return render(request, self.template, {"form":form})
              
        
class ProposalEvaluationView(View):
    
    form = ProposalEvaluationForm
    template = "components/staffs/evaluations/proposal_evaluation.html"
    success_template="components/success-dialog.html"
    
    def get(self, request, student_id, *args, **kwargs):
        user = self.request.user
        if user.is_authenticated and user.profile.can_evaluate():
            student = Student.objects.get(id=str(student_id))
            context = {
                "student": student,
                "form": self.form()
            }
            return render(request, self.template, context)
        return  redirect("authentication:evaluator-login")   
    
    def post(self, request, student_id, *args, **kwargs):
        student = Student.objects.get(id=str(student_id))
        form = self.form(data=request.POST)
        if form.is_valid():
            # Validate secret phrase to authorize signing
            if not form.validate_evaluator(self.request.user.profile):
                form.add_error("secret", "Invalid Secret Phrase")
                context = {
                    "student":student,
                    "form":form
                }
                return render(request, self.template, context)
            
            else:
                staff = request.user.profile
            
                # Validate that staff hasn't evaluated student before
                if form.can_evaluate(student, staff):    
                    form.evaluate(
                        student=student,
                        staff=request.user.profile,
                    )
                    context = {
                        "message": f"Thank you for evaluating Student: {student.matric_number}"
                    }
                    return render(request, self.success_template, context)
                else:
                    form.add_error("secret", "Invalid")
                    context = {
                        "message":"YOU HAVE ALEARDY EVALUATED this student",
                    }
                    return render(request, self.success_template, context)
        else:
            context = {
                "student":student,
                "form":form,
                "form_error":"Invalid response(s)! Please Check"
            }
            return render(request, self.template, {"form": form})

            
class WorkProgressEvaluationView(View):
    
    form = WorkProgressEvaluationForm
    template = "components/staffs/evaluations/work_progress_evaluation.html"
    success_template="components/success-dialog.html"
    
    def get(self, request, student_id, *args, **kwargs):
        user = self.request.user
        if user.is_authenticated and user.profile.can_evaluate():
            student = Student.objects.get(id=str(student_id))
            context = {
                "student": student,
                "form": self.form()
            }
            return render(request, self.template, context)
        return  redirect("authentication:evaluator-login")   
    
    def post(self, request, student_id, *args, **kwargs):
        student = Student.objects.get(id=str(student_id))
        form = self.form(data=request.POST)
        if form.is_valid():
            
            # Validate secret phrase to authorize signing
            if not form.validate_evaluator(self.request.user.profile):
                form.add_error("secret", "Invalid Secret Phrase")
                context = {
                    "student":student,
                    "form":form
                }
                return render(request, self.template, context)
            
            else:
                staff = request.user.profile
            
                # Validate that staff hasn't evaluated student before
                if form.can_evaluate(student, staff):    
                    form.evaluate(
                        student=student,
                        staff=request.user.profile,
                    )
                    context = {
                        "message": f"Thank you for evaluating Student: {student.matric_number}"
                    }
                    return render(request, self.success_template, context)
                else:
                    form.add_error("secret", "Invalid")
                    context = {
                        "message":"YOU HAVE ALEARDY EVALUATED this student",
                    }
                    return render(request, self.success_template, context)
        else:
            context = {
                "student":student,
                "form":form,
                "form_error":"Invalid response(s)! Please Check"
            }
            return render(request, self.template, {"form": form})


class InternalDefenseEvaluationView(View):
    
    form = DefenseEvaluationForm
    template = "components/staffs/evaluations/defense_evaluation.html"
    success_template="components/success-dialog.html"
    
    def get(self, request, student_id, *args, **kwargs):
        user = self.request.user
        if user.is_authenticated and user.profile.can_evaluate():
            student = Student.objects.get(id=str(student_id))            
            context = {
                "student": student,
                "form": self.form(),
                "internal":True,
            }     
            return render(request, self.template, context)
        return  redirect("authenticator:evaluator-login")   
    
    def post(self, request, student_id, *args, **kwargs):
        student = Student.objects.get(id=str(student_id))
        form = self.form(data=request.POST)
        
        if form.is_valid():

            # Validate secret phrase to authorize signing
            if not form.validate_evaluator(self.request.user.profile):
                form.add_error("secret", "Invalid Secret Phrase")
                context = {
                    "student":student,
                    "form":form
                }
                return render(request, self.template, context)
            
            else:
                staff = request.user.profile
            
                # Validate that staff hasn't evaluated student before
                if form.can_evaluate(student, staff):    
                    form.evaluate(student, request.user.profile)
                    
                    context = {
                        "message": f"Thank you for evaluating Student: {student.matric_number}",
                        "button_url": ""
                    }
                    return render(request, self.success_template, context)
                
                else:
                    form.add_error("secret", "Invalid")
                    context = {
                        "message":"YOU HAVE ALEARDY EVALUATED this student",
                        "button_url": ""
                    }
                    return render(request, self.success_template, context)
        else:
            context = {
                "student":student,
                "form":form,
                "form_error":"Invalid response(s)! Please Check"
            }
            return render(request, self.template, {"form": form})

