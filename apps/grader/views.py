from django.shortcuts import render
from .forms import (
    StudentDetailsForm
)
from django.views import View
from django.http import HttpResponse





class StudentDetailsCreationView(View):
    
    form = StudentDetailsForm
    # template = "students/student_form.html"
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