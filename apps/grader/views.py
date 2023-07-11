from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import (
    StudentRegistrationForm,
    StaffRegistrationForm,
    StudentEvaluationSearchForm,
    ProposalEvaluationForm,
    WorkProgressEvaluationForm,
    DefenseEvaluationForm,
    ExternalDefenseEvaluationForm,
    ProjectApprovalForm,
    StudentSearchForm,
    
)
from .models import (
    Student,
    Project,
    Staff,
    FinalYearSession,
)
from apps.utils.utils import query_params
from django.views import View
from django.http import HttpResponse
from apps.utils.constants import (
    EVALUATION_TYPES,
    STUDENT_TABLE_HEADER
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin




class AuthenicatedBaseView(LoginRequiredMixin, View):
    
    def get_login_url(self):
        return reverse("authentication:login")


def landing_page(request):
    context = {
        "title":"FY Project Grader",
        "subtext":"Portal",
        "navs": [
            (reverse("grader:student-router"), "group.svg", "Students"),
            (reverse("grader:staff-router"), "staff.svg", "Staffs & Evaluators"),
        ]
    }
    return render(request, "index.html", context)


def student_router(request):
    context = {
        "title":"FY Project Grader",
        "subtext":"Student Portal",
        "navs": [
            (reverse("grader:student-registration"), "group.svg", "Create Project Topic"),
            (reverse("grader:student-project-status"), "group.svg", "Project Status"),
        ]
    }
    return render(request, "index.html", context)


@login_required(login_url="authentication:login")
def staff_router(request):
    context = {
        "title":"FY Project Grader",
        "subtext":"Staff Portal",
        "navs": [
            (reverse("grader:dashboard"), "dashboard.svg", "Dashboard"),
            
        ]
    }
    return render(request, "index.html", context)






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


class StudentProjectStatus(View):
    
    form = StudentSearchForm
    template = "components/search_form.html"
    success_template = "components/students/project_status.html"
    
    def get(self, request, *args, **kwargs):
        form = self.form()
        return render(request, self.template, {"form":form})
    
    def post(self, request, *args, **kwargs):
        form = self.form(data=request.POST)
        if form.is_valid():
            student, found = form.search()
            if found:
                context = {
                    "project":student.project,
                }
                return render(request,self.success_template, context)
                
            else:
                form.add_error("student", "Not Found!")
                context = {
                    "message":"Sorry, Student not found.",
                    "form":form
                }
                return render(request, self.template, context)
        
        else:
            return render(request, self.template, {"form":form})
      
    
    
    
# Staff Views        
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



# Student evalution view by staffs
class StudentEvaluationSearchView(View):
    
    form = StudentEvaluationSearchForm
    template = "components/search_form.html"
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:    
            form = self.form()
            return render(request, self.template, {"form":form})
        return redirect("authentication:evaluator-login")
    
    def post(self, request, *args, **kwargs):
        form = self.form(data=request.POST)
        if form.is_valid():
            student, found = form.search()
            evaluation = form.cleaned_data.get("type")
            if found:
                # check if student has been evaluated to their max
                if form.can_evaluate_student():
                    if EVALUATION_TYPES[evaluation] == EVALUATION_TYPES["proposal"]:
                        return redirect("grader:proposal-evaluation", student.id)
                    
                    elif EVALUATION_TYPES[evaluation] == EVALUATION_TYPES["work_progress"]:
                        return redirect("grader:work-progress-evaluation", student.id)
                    
                    elif EVALUATION_TYPES[evaluation] == EVALUATION_TYPES["internal_defence"]:
                        return redirect(reverse("grader:internal-defense-evaluation", args=[student.id]))
                    
                    elif EVALUATION_TYPES[evaluation] == EVALUATION_TYPES["external_defence"]:
                        return redirect(reverse("grader:external-defense-evaluation", args=[student.id]))
                else:
                    form.add_error("student", "Not Found!")
                    context = {
                        "message":"Sorry, Maximum Evaluation reached.",
                        "form":form
                    }
                    return render(request, self.template, context)
                
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
                        "message": f"Thank you for evaluating Student: {student.matric_number}",
                        "button":True,
                        "button_link":reverse("grader:search-for-student"),
                        "title":"Next Evaluation"
                        
                    }
                    return render(request, self.success_template, context)
                else:
                    context = {
                        "message":"YOU HAVE ALEARDY EVALUATED this student",
                        "button":True,
                        "button_link":reverse("grader:search-for-student"),
                        "title":"Next Evaluation"
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
                        "message": f"Thank you for evaluating Student: {student.matric_number}",
                        "button":True,
                        "button_link":reverse("grader:search-for-student"),
                        "title":"Next Evaluation"
                    }
                    return render(request, self.success_template, context)
                else:
                    form.add_error("secret", "Invalid")
                    context = {
                        "message":"YOU HAVE ALEARDY EVALUATED this student",
                        "button":True,
                        "button_link":reverse("grader:search-for-student"),
                        "title":"Next Evaluation"
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
        return  redirect("authentication:evaluator-login")   
    
    def post(self, request, student_id, *args, **kwargs):
        student = Student.objects.get(id=str(student_id))
        form = self.form(data=request.POST)
        
        if form.is_valid():

            staff = request.user.profile
            # Validate secret phrase to authorize signing
            if not form.validate_evaluator(staff):
                form.add_error("secret", "Invalid Secret Phrase")
                context = {
                    "student":student,
                    "form":form
                }
                return render(request, self.template, context)
            
            else:
                
                # Validate that staff hasn't evaluated student before
                if form.can_evaluate(student, staff):    
                    form.evaluate(student, staff)
                    
                    context = {
                        "message": f"Thank you for evaluating Student: {student.matric_number}",
                        "button":True,
                        "button_link":reverse("grader:search-for-student"),
                        "title":"Next Evaluation"
                    }
                    return render(request, self.success_template, context)
                
                else:
                    context = {
                        "message":"YOU HAVE ALEARDY EVALUATED this student",
                        "button":True,
                        "button_link":reverse("grader:search-for-student"),
                        "title":"Next Evaluation"
                    }
                    return render(request, self.success_template, context)
        else:
            context = {
                "student":student,
                "form":form,
                "internal":True,
            }
            return render(request, self.template, context)


class ExternalDefenseEvaluationView(View):
    
    form = ExternalDefenseEvaluationForm
    template = "components/staffs/evaluations/defense_evaluation.html"
    success_template="components/success-dialog.html"
    
    def get(self, request, student_id, *args, **kwargs):
        user = self.request.user
        if user.is_authenticated and user.profile.can_evaluate():
            student = Student.objects.get(id=str(student_id))            
            context = {
                "student": student,
                "form": self.form(),
            }     
            return render(request, self.template, context)
        return  redirect("authentication:evaluator-login")   
    
    def post(self, request, student_id, *args, **kwargs):
        student = Student.objects.get(id=str(student_id))
        form = self.form(data=request.POST)
        
        if form.is_valid():
            staff = self.request.user.profile

            # Validate secret phrase to authorize signing
            if not form.validate_evaluator(staff):
                form.add_error("secret", "Invalid Secret Phrase")
                context = {
                    "student":student,
                    "form":form
                }
                return render(request, self.template, context)
            
            else:
                # Validate that Student hasn't been evaluated before
                if form.can_evaluate(student):    
                    form.evaluate(student, staff)
                    
                    context = {
                        "message": f"Thank you for evaluating Student: {student.matric_number}",
                        "button":True,
                        "button_link":reverse("grader:search-for-student"),
                        "title":"Next Evaluation"
                    }
                    return render(request, self.success_template, context)
                
                else:
                    context = {
                        "message":"Student has already been Evaluated.",
                        "button":True,
                        "button_link":reverse("grader:search-for-student"),
                        "title":"Next Evaluation"
                    }
                    return render(request, self.success_template, context)
        else:
            context = {
                "student":student,
                "form":form,
                "form_error":"Invalid response(s)! Please Check"
            }
            return render(request, self.template, {"form": form})


# Staff Dashboard views

class DashboardHomeView(AuthenicatedBaseView):
    
    admin_template = "components/dashboard/admin-home.html"
    supervisor_template = "components/dashboard/table.html"
    
    
    def get(self, request, *args, **kwargs):
        projects = Project.objects.filter(
            completed=False)
        staff = self.request.user.profile
        
        if self.request.user.is_superuser:
            staff_list = Staff.objects.filter(active=True)
            
            context = {
                "navs": [
                    (True, "dashboard_white.svg", reverse("grader:dashboard"), "Home"),
                    (False, "group.svg", reverse("grader:dashboard-student"), "Students"),
                    (False, "staff.svg", "#", "Staffs"),
                    (False, "calendar.svg", "#", "Session"),
                ],
                "session":FinalYearSession.objects.filter(active=True).first(),
                "total_students":projects.count(),
                "approved_topics":projects.filter(supervisor_approval=True).count(),
                "total_staffs":staff_list.filter(staff_type="Supervisor_and_Evaluator").count(),
                "total_evaluators":staff_list.count(),
                "dashboard_title":"Home",
                "dashboard_user":f"Cordinator {staff.first_name}",
            }
            return render(request, self.admin_template, context)
            
        else:
            return redirect("grader:dashboard-student")
    
       
class DashboardStudentView(AuthenicatedBaseView):
    
    template = "components/dashboard/table.html"
    
    def get(self, request, *args, **kwargs):
        projects = Project.objects.filter(
            completed=False)
        staff = self.request.user.profile

        context = {
            "headers": STUDENT_TABLE_HEADER,
            "dashboard_title":"Students",   
        }
        
        if self.request.user.is_superuser:
            context.update({
                "navs": [
                    (False, "dashboard.svg", reverse("grader:dashboard"), "Home"),
                    (True, "group_white.svg", reverse("grader:dashboard-student"), "Students"),
                    (False, "staff.svg", "#", "Staffs"),
                    (False, "calendar.svg", "#", "Session"),
                ],
                "projects": projects.filter(supervisor=staff),
                "dashboard_user":f"Cordinator {staff.first_name}",
            })
            return render(request, self.template, context)
            
        else:
            context.update({
                "navs": [
                    (True, "group_white.svg", reverse("grader:dashboard-student"), "Students"),
                ],
                "projects": projects.filter(supervisor=staff),
                "dashboard_user":f"Supervisor {staff.first_name}", 
            })
            return render(request, self.template, context)

  
  
class DashboardStudentDetailView(AuthenicatedBaseView):
    
    form = ProjectApprovalForm
    template = "components/dashboard/project-details.html"
    
    
    def get(self, request, project_id, *args, **kwargs):
        
        project = Project.objects.get(id=project_id)
        staff = self.request.user.profile
        context = {
            "project":project,
            "objectives":project.get_objectives(),
            "dashboard_title":"Students",
            "form":self.form(),
        }
        if self.request.user.is_superuser:
            context.update({
                "navs": [
                    (False, "dashboard.svg", reverse("grader:dashboard"), "Home"),
                    (True, "group_white.svg", reverse("grader:dashboard-student"), "Students"),
                    (False, "staff.svg", "#", "Staffs"),
                    (False, "calendar.svg", "#", "Session")
                ],
                "dashboard_user":f"Cordinator {staff.first_name}",
            })
            
        else:
            context.update({
                "navs": [
                    (True, "group_white.svg", reverse("grader:dashboard-student"), "Students"),
                ],
                "dashboard_user":f"Supervisor {staff.first_name}",
            })
    
        return render(request, self.template, context)

    def post(self, request, project_id, *args, **kwargs):
        project = Project.objects.get(id=project_id)
        staff = self.request.user.profile
        form = self.form(data=request.POST)
        
        if form.is_valid() and form.validate_evaluator(staff):
            form.perform_approval(project, staff.user.is_superuser)
            return redirect("grader:dashboard-student")
        
        else:
            context = {
                "project":project,
                "objectives":project.get_objectives(),
                "dashboard_title":"Students",
                "form":form,
                }
            if self.request.user.is_superuser:
                context.update({
                    "navs": [
                        (False, "dashboard.svg", reverse("grader:dashboard"), "Home"),
                        (True, "group_white.svg", reverse("grader:dashboard-student"), "Students"),
                        (False, "staff.svg", "#", "Staffs"),
                        (False, "calendar.svg", "#", "Session")
                    ],
                    "dashboard_user":f"Cordinator {staff.first_name}",
                })
                
            else:
                context.update({
                    "navs": [
                        (True, "group_white.svg", reverse("grader:dashboard-student"), "Students"),
                    ],
                    "dashboard_user":f"Supervisor {staff.first_name}",
                })
        
            return render(request, self.template, context)
            
            
            
            
    
def hello(request):
    
    form = ProjectApprovalForm()
    context = {
        "navs": [
            (True, "dashboard.svg", "link", "Home"),
            (False, "person.svg", "link", "Students"),
            (False, "staff.svg", "link", "Staffs"),
            (False, "calendar.svg", "link", "Session"),
        ],
        # "project":my_project,
        "form":form,
        "dashboard_title":"Students",
        "dashboard_user":"Supervisor",
    
    }
    return render(request, "components/dashboard/project-details.html", context)