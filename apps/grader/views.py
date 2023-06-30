from django.shortcuts import render
from .forms import (
    StudentDetailsForm
)
from django.views import View
from django.http import HttpResponse





class StudentDetailsCreationView(View):
    
    form = StudentDetailsForm
    # template = "students/student_form.html"
    template="components/form.html"
    
    def get(self, request, *args, **kwargs):
        form = self.form()
        return render(request, self.template, {"form":form})
    
    def post(self, request, *args, **kwargs):
        form = self.form(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Form successfully submitted")
        else:
            return render(request, self.template, {"form":form})