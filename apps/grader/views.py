from django.shortcuts import render
from .forms import (
    StudentRegistrationForm,
    StaffRegistrationForm,
    StudentEvaluationSearchForm
)
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
            # import pdb; pdb.set_trace()
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
    template = "demo.html"
    evaluation_template = ""
    
    def get(self, request, *args, **kwargs):
        form = self.form()
        return render(request, self.template, {"form":form})
    
    def post(self, request, *args, **kwargs):
        form = self.form(data=request.POST)
        if form.is_valid():
            student, found = form.search()
            if found:
                return HttpResponse("Student found now render template")
            else:
                form.add_error("student", "Not Found!")
                context = {
                    "message":"Sorry, student not found.",
                    "form":form
                }
                return render(request, self.template, context)
        
        else:
            return render(request, self.template, {"form":form})