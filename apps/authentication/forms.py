from django import forms
from django.contrib.auth import login
from django.contrib.auth import authenticate
from apps.utils.security import validate_secret
from django.contrib.auth.forms import AuthenticationForm




class EvaluatorAuthenticationForm(AuthenticationForm):
    secret = forms.CharField()
    
    
    def authenticate(self, request):
        email = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        secret = self.cleaned_data.get("secret")
        
        # Authenticate user
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            
            # Validate staff secret            
            staff = user.profile
            if validate_secret(secret, staff.secret):
                login(request, user)
                return True
            else:
                return False
        else:
            return False
            
            
            
        
        
        
    