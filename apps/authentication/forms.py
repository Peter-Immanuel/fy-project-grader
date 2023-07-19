from django import forms
from django.contrib.auth import login
from django.contrib.auth import authenticate
from apps.utils.security import validate_secret
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model



User = get_user_model()
class EvaluatorAuthenticationForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
        required=True
    )
    secret = forms.CharField()
    
    
    def authenticate(self, request):
        email = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        secret = self.cleaned_data.get("secret")
        
        # Authenticate user
        user = authenticate(request, username=email.lower(), password=password)
        
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
            
            
class ResetStaffDetailsViewForm(forms.Form):   
    email = forms.EmailField()
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
        required=True
    )
    secret = forms.CharField()
    
    
    def clean_email(self):
        user = User.objects.filter(email=self.cleaned_data.get("email"))
        if not user.exists():
            raise forms.ValidationError(_("Sorry staff not found"))
        return user
    
    def reset_details(self):
        staff = self.cleaned_data.get("email").first().profile
        
        staff.reset_details(
            password=self.cleaned_data.get("password"),
            secret=self.cleaned_data.get("secret"),
        )
        return 
       
        
        
        
        
    