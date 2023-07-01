from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import EvaluatorAuthenticationForm



class AdminAuthenticationView(View):
    
    form = AuthenticationForm
    template = "demo.html"
    
    def get(self, request, *args, **kwargs):
        form = self.form()
        return render(request, self.template, {"form":form})
    
    def post(self, request, *args, **kwargs):
        form = self.form(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=email, password=password)
            
            if user is not None and user.is_superuser:
                login(request, user)
                
                # Todo: Replace with admin dashboard
                return HttpResponse("Logged in successfully")
            
            elif user is not None and not user.is_superuser:
                context = {
                    "message":"Sorry you don't have access!",
                    "form":form
                }
                return render(request, self.template, context)
                 
            else:
                form.add_error("username", "Invalid email or password")
                context = {
                    "message":"Sorry User not found",
                    "form":form
                }
                return render(request, self.template, context)
            
        else:
            return render(request, self.template, {"form":form})
        
        
        
class EvaluatorAuthenticationView(View):
    
    form = EvaluatorAuthenticationForm
    template = "demo.html"
    
    def get(self, request, *args, **kwargs):
        form = self.form()
        return render(request, self.template, {"form":form})
    
    def post(self, request, *args, **kwargs):
        form = self.form(data=request.POST)
        if form.is_valid():
            
            is_authenticated = form.authenticate(request)         
            if is_authenticated:
                # Todo: Replace with evaluator's dashboard
                return HttpResponse("Evaluateor Logged in successfully")
            
            else:
                form.add_error("username", "Invalid email, password or secret phrase")
                context = {
                    "message":"Sorry User not found",
                    "form":form
                }
                return render(request, self.template, context)
        else:
            return render(request, self.template, {"form":form})
        