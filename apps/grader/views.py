from django.shortcuts import render, redirect
from .forms import (
    StudentRegistrationForm,
    StaffRegistrationForm,
    StudentEvaluationSearchForm,
    ProposalEvaluationForm,
    WorkProgressEvaluationForm,
)
from .models import Student
from apps.utils.utils import query_params
from django.views import View
from django.http import HttpResponse





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
    success_template="components/success-dialog.html"
    
    def get(self, request, *args, **kwargs):
        form = self.form()
        return render(request, self.template, {"form":form})
    
    def post(self, request, *args, **kwargs):
        form = self.form(data=request.POST)
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
    evaluation_template = ""
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:   
            print(self.request.user)     
            form = self.form()
            return render(request, self.template, {"form":form})
        return redirect("authenticator:evaluator-login")
    
    def post(self, request, *args, **kwargs):
        form = self.form(data=request.POST)
        if form.is_valid():
            student, found = form.search()
            if found:
                return redirect("grader:evaluation-form", student.id)
            else:
                form.add_error("student", "Not Found!")
                context = {
                    "message":"Sorry, Student not found.",
                    "form":form
                }
                return render(request, self.template, context)
        
        else:
            return render(request, self.template, {"form":form})
        
        
        
class EvaluationView(View):
    
    form = ProposalEvaluationForm
    template = "components/staffs/proposal_evaluation.html"
    
    def get(self, request, *args, **kwargs):
        student = Student.objects.get(id=str(kwargs.get("student_id")))
        context = {
            "student": student,
            "form": self.form()
        }
        return render(request, self.template, context)
    
    
    def post(self, request, *args, **kwargs):
        form = self.form(data=request.POST)
        if form.is_valid():
            return HttpResponse("wow!")
        
        else:
            return render(request, self.template, {"form": form})