from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.generic.edit import CreateView
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from .forms import EvaluatorAuthenticationForm




class DevPanelView(CreateView):
    template_name = "demo.html"
    model = get_user_model()
    fields = ["email", "password"]
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        
        if form.is_valid():
            form.cleaned_data.update(
                {"is_staff":True,
                "is_superuser": True}
            )
            self.model.objects.create_superuser(
                email=form.cleaned_data.pop("email"),
                password=form.cleaned_data.pop("password"),
                **form.cleaned_data,
            )
            
            return HttpResponse("success")
        return HttpResponse(form.errors)
    
    


class AdminAuthenticationView(View):
    
    form = AuthenticationForm
    template = "components/staffs/login.html"
    
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
                form.add_error("username", "Not Authorized")
                context = {
                    "message":"Sorry, you're not authorized",
                    "form":form
                }
                return render(request, self.template, context)
            
        else:
            context = {
                "message": "Invalid credentials provided",
                "form":form
            }
            
            return render(request, self.template, context)
        
              
class EvaluatorAuthenticationView(View):
    
    form = EvaluatorAuthenticationForm
    template = "components/staffs/login.html"
    success_template = "components/search_form.html"
    
    def get(self, request, *args, **kwargs):
        form = self.form()
        return render(request, self.template, {"form":form})
    
    def post(self, request, *args, **kwargs):
        
        form = self.form(data=request.POST)
        
        if form.is_valid():
            
            is_authenticated = form.authenticate(request)         
            if is_authenticated:
                return redirect("grader:dashboard")
            
            else:
                form.add_error("username", "Invalid email, password or secret phrase")
                context = {
                    "message":"Sorry User not found",
                    "form":form
                }
                return render(request, self.template, context)
        else:
            context = {
                "message":"Sorry User not found",
                "form":form
            }
            
            return render(request, self.template, context)
 
 
def logout_admin(request):
    logout(request)
    return redirect("authentication:login")