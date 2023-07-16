import uuid
from django.db import models, transaction
from apps.utils.constants import (
    STAFF_TITLE, 
    STAFF_TYPE,
    GENDER,
    APPROVAL_STATUS,
)
from passlib.context import CryptContext
from django.contrib.auth import get_user_model


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

User = get_user_model()

# BaseModels
class TimeStampModel(models.Model):
    ''' Abstract Base Model to keep id, created_at and updated_at fields '''
    
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        abstract = True
             
        
class Faculty(TimeStampModel):
    ''' Model describing faculties a.k.a schools in FUT minna '''
    
    name = models.CharField(max_length=500)
    short_name = models.CharField(max_length=50)
    inauguration_date = models.DateField(null=True, blank=True)
    active = models.BooleanField(
        default=True, help_text="Indicates if the faculty still exisits or not")
    
    
    class Meta:
        verbose_name = "Faculty"
        verbose_name_plural = "Faculties"
    
    def __str__(self):
        return self.short_name

        
class Department(TimeStampModel):
    ''' Model describing deparments in a.k.a schools in FUT minna '''
    
    name = models.CharField(max_length=500)
    short_name = models.CharField(max_length=50)
    inauguration_date = models.DateField(null=True, blank=True)
    active = models.BooleanField(
        default=True, help_text="Indicates if the department still exisits or not")
    faculty = models.ForeignKey(Faculty, related_name="faculties", on_delete=models.CASCADE)
    cordinator = models.ForeignKey(
        "Staff", related_name="deparment_cordinator", on_delete=models.CASCADE, null=True, blank=True)
    
    
    class Meta:
        verbose_name = "Department"
        verbose_name_plural = "Departments"
        
    def __str__(self):
        return self.short_name
        

class FinalYearSession(TimeStampModel):
    """ Model describing accademic session and each department's project cordinator"""
    
    year = models.CharField(max_length=50)
    active = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Final Year Session"
        verbose_name_plural = "Final Year Sessions"
    
    def __str__(self):
        return self.year
    
    
    

class StaffManager(models.Manager):
    """ Staff Model manager to create a staff and it's corresponding user instance """
    
    def create_staff_profile(self, password, **extra_fields):
        secret = extra_fields.pop("secret")
        
        # Hash Secret phrase
        extra_fields.update({
            "secret": pwd_context.hash(secret)
        })
        
        with transaction.atomic():
            staff_user = User.objects.create_user(extra_fields["email"], password)
            staff = Staff.objects.create(user=staff_user, **extra_fields)
            return staff
        
    
class Staff(TimeStampModel):
    """ Model describing Staff within each department """
    
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    title = models.CharField(max_length=50, choices=STAFF_TITLE)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    staff_type = models.CharField(choices=STAFF_TYPE, max_length=50)
    gender = models.CharField(choices=GENDER, max_length=20)
    signature = models.FileField(upload_to="staff/signatures/", null=True, blank=True)
    department = models.ForeignKey(
        Department, related_name="staffs", on_delete=models.SET_NULL, null=True, blank=True)
    faculty = models.ForeignKey(
        Faculty, related_name="staffs", on_delete=models.SET_NULL, null=True, blank=True)
    active = models.BooleanField(
        default=True, help_text="Indicates if the staff is available or not (E.g a case where they leave the country or dies)")
    secret = models.TextField(help_text="Text used to validate the use of signature")
    
    objects = StaffManager()
    
    def __str__(self):
        return self.get_full_name()
        
    def get_full_name(self):
        return (
            f"{self.title} {self.first_name} {self.middle_name} {self.last_name}" 
            if self.middle_name else 
            f"{self.title} {self.first_name} {self.last_name}" 
        )
 
    def can_evaluate(self):
        if self.staff_type in ["Internal_Evaluator","External_Evaluator","Supervisor_and_Evaluator"]:
            return True
        return False
        



class StudentManager(models.Manager):
    
    def create_student_details(self, title, supervisor, **extra_fields):
        
        with transaction.atomic():
            description = extra_fields.pop("description")
            aims = extra_fields.pop("aims")
            objectives = extra_fields.pop("objectives")
            student = self.model.objects.create(**extra_fields)
            
            Project.objects.create(
                student=student,
                title=title,
                supervisor=supervisor,
                department=student.department,
                faculty=student.faculty,
                aims=aims,
                description=description,
                objectives=objectives,
                session=student.session,
            )
            return student

    
class Student(TimeStampModel):
    """Model describing Final year students within each department """
    
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    matric_number = models.CharField(max_length=100, unique=True)
    gender = models.CharField(choices=GENDER, max_length=20)
    active = models.BooleanField(
        default=True, help_text="Indicates if the student is available or not (E.g a case where they leave the country or dies)")
    session = models.ForeignKey(
        FinalYearSession, related_name="students", on_delete=models.CASCADE)
    department = models.ForeignKey(
        Department, related_name="students", on_delete=models.CASCADE)
    faculty = models.ForeignKey(
        Faculty, related_name="students", on_delete=models.CASCADE)
    graduated = models.BooleanField(
        default=False, help_text="Indicates if the student has graduated or not")
    
    
    objects = StudentManager()
    
    def __str__(self):
        return self.get_full_name()
        
    def get_full_name(self):
        return (
            f"{self.first_name} {self.middle_name} {self.last_name} | {self.matric_number}" 
            if self.middle_name else 
            f"{self.first_name} {self.last_name} | {self.matric_number}" 
        )
        
    def get_name(self):
        return (
            f"{self.first_name} {self.middle_name} {self.last_name}" 
            if self.middle_name else 
            f"{self.first_name} {self.last_name}" 
        ) 
  
        
class Project(TimeStampModel):
    """ Model describing each student's project """
    
    student = models.OneToOneField(
        Student, related_name="project", on_delete=models.CASCADE)
    title = models.TextField()
    aims = models.TextField(null=True, blank=True)
    objectives = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    supervisor = models.ForeignKey(
        Staff, related_name="projects", on_delete=models.CASCADE)
    co_supervisor = models.ForeignKey(
        Staff, related_name="co_projects", on_delete=models.CASCADE, null=True, blank=True)
    department = models.ForeignKey(Department, related_name="department_projects", on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, related_name="faculty_projects", on_delete=models.CASCADE)
    
    session = models.ForeignKey(FinalYearSession, related_name="projects", on_delete=models.CASCADE)
    
    proposal_score = models.IntegerField(
        null=True, blank=True, help_text="This is the average of 3 proposal grading scores")
    work_progress_score = models.IntegerField(
        null=True, blank=True, help_text="This is the average of 3 project work progress scores")
    internal_defense_score = models.IntegerField(
        null=True, blank=True, help_text="This is the average of 3 internal defense scores")
    external_defense_score = models.IntegerField(
        null=True, blank=True, help_text="This is the average of 3 internal defense scores")
    
    project_score = models.IntegerField(
        null=True, blank=True, help_text="This is the Average score of all 4 scores category")
    
    device_score = models.IntegerField(
        null=True, blank=True, help_text="This is the score given to the student device (Hardware/Software integration)")
    
    supervisor_comment = models.TextField(null=True, blank=True)
    supervisor_approval_status = models.CharField(max_length=20, choices=APPROVAL_STATUS, default="Pending")
    supervisor_approval = models.BooleanField(default=False)
    supervisor_score = models.IntegerField(
        null=True, blank=True, help_text="This is the score given to a student's project by their supervisor")
    
    cordinator_comment = models.TextField(null=True, blank=True)
    cordinator_approval_status = models.CharField(max_length=20, choices=APPROVAL_STATUS, default="Pending")
    cordinator_approval = models.BooleanField(default=False)
    
    completed = models.BooleanField(default=False)
    
    
    def __str__(self):
        return f"{self.title} by {self.student.matric_number}"
       
    def get_objectives(self):
        return self.objectives.split("-")
    
    def approve_by_supervisor(self, status, comment):
        self.supervisor_approval = status
        self.supervisor_comment = comment
        
        if status:
            self.supervisor_approval_status = "Approved"
        else:
            self.supervisor_approval_status = "Not Approved"
        self.save()
        
    def approve_by_cordinator(self, status, comment):
        self.cordinator_approval = status
        self.cordinator_comment = comment
        
        if status:
            self.cordinator_approval_status = "Approved"
        else:
            self.cordinator_approval_status = "Not Approved"
        self.save()
    
    def approve_cordinator_student(self, status, comment):
        self.supervisor_approval = status
        self.supervisor_comment = comment
        
        self.cordinator_approval = status
        self.cordinator_comment = comment
        
        if status:
            self.cordinator_approval_status = "Approved"
            self.supervisor_approval_status = "Approved"
        else:
            self.cordinator_approval_status = "Not Approved"
            self.supervisor_approval_status = "Not Approved"
        
        self.save()
             
    def update_records(self, updates):
        
        for key, value in updates.items():
            if hasattr(self, key):
                setattr(self, key, value)
        
        self.save()
        return self
        
        
    
    
class ProjectProposalGrading(TimeStampModel):
    """ Model describing each student's project proposal score """
    
    session = models.ForeignKey(
        FinalYearSession, related_name="project_proposal_gradings", on_delete=models.CASCADE)
    faculty = models.ForeignKey(
        Faculty, related_name="project_proposal_gradings", on_delete=models.CASCADE)
    department = models.ForeignKey(
        Department, related_name="project_proposal_gradings", on_delete=models.CASCADE)
    
    student = models.ForeignKey(
        Student, related_name="project_proposal_gradings", on_delete=models.CASCADE)
    project = models.ForeignKey(
        Project, related_name="project_proposal_gradings", on_delete=models.CASCADE)
    
    objective_scope = models.IntegerField()
    research_methodology = models.IntegerField()
    literature_review = models.IntegerField()
    communication_skills = models.IntegerField()
    total = models.IntegerField()
    
    evaluator = models.ForeignKey(
        Staff, related_name="project_proposal_grading_evaluations", on_delete=models.CASCADE)
    comment = models.TextField(null=True, blank=True)
    date_evaluated = models.DateField()
    signed = models.BooleanField()
    
    
    class Meta:
        verbose_name = "Project Proposal Grading"
        verbose_name_plural = "Project Proposal Gradings"
    
    def __str__(self):
        return f"Project Proposal Grading for {self.project} by {self.evaluator}"    
        
    
class ProjectWorkProgress(TimeStampModel):
    """ Model describing each student's project work progress score """
    
    session = models.ForeignKey(
        FinalYearSession, related_name="project_work_progress_gradings", on_delete=models.CASCADE)
    faculty = models.ForeignKey(
        Faculty, related_name="project_work_progress_gradings", on_delete=models.CASCADE)
    department = models.ForeignKey(
        Department, related_name="project_work_progress_gradings", on_delete=models.CASCADE)
    
    student = models.ForeignKey(
        Student, related_name="project_work_progress_gradings", on_delete=models.CASCADE)
    project = models.ForeignKey(
        Project, related_name="project_work_progress_gradings", on_delete=models.CASCADE)
    
    project_methodology = models.IntegerField()
    preliminary_result = models.IntegerField()
    communication_skills = models.IntegerField()
    total = models.IntegerField()
    
    evaluator = models.ForeignKey(
        Staff, related_name="project_work_progress_grading_evaluations", on_delete=models.CASCADE)
    comment = models.TextField(null=True, blank=True)
    date_evaluated = models.DateField()
    signed = models.BooleanField()
    
    
    class Meta:
        verbose_name = "Project Work Progress Grading"
        verbose_name_plural = "Project Work Progress Gradings"
        
    def __str__(self):
        return f"Project Work Progress Grading for {self.project} by {self.evaluator}"
    
    
class InternalDefense(TimeStampModel):
    """ Model describing each student's project internal defense score """
    
    session = models.ForeignKey(
        FinalYearSession, related_name="internal_defense_gradings", on_delete=models.CASCADE)
    faculty = models.ForeignKey(
        Faculty, related_name="internal_defense_gradings", on_delete=models.CASCADE)
    department = models.ForeignKey(
        Department, related_name="internal_defense_gradings", on_delete=models.CASCADE)
    
    student = models.ForeignKey(
        Student, related_name="internal_defense_gradings", on_delete=models.CASCADE)
    project = models.ForeignKey(
        Project, related_name="internal_defense_gradings", on_delete=models.CASCADE)
    
    problem_statement = models.IntegerField()
    project_methodology = models.IntegerField()
    result_discussion = models.IntegerField()
    conclusion = models.IntegerField()
    communication_skills = models.IntegerField()
    device_score = models.IntegerField(null=True, blank=True)
    total = models.IntegerField()
    
    evaluator = models.ForeignKey(
        Staff, related_name="internal_defense_grading_evaluations", on_delete=models.CASCADE)
    comment = models.TextField(null=True, blank=True)
    date_evaluated = models.DateField()
    signed = models.BooleanField()
    
    
    class Meta:
        verbose_name = "Internal Project Defense Grading"
        verbose_name_plural = "Internal Project Defense Grading"
        
    def __str__(self):
        return f"Internal Project Defense Grading for {self.project.title} by {self.evaluator}"
     

class ExternalDefense(TimeStampModel):
    """ Model describing each student's project External defense score """
    
    session = models.ForeignKey(
        FinalYearSession, related_name="external_defense_gradings", on_delete=models.CASCADE)
    faculty = models.ForeignKey(
        Faculty, related_name="external_defense_gradings", on_delete=models.CASCADE)
    department = models.ForeignKey(
        Department, related_name="external_defense_gradings", on_delete=models.CASCADE)
    
    student = models.ForeignKey(
        Student, related_name="external_defense_gradings", on_delete=models.CASCADE)
    project = models.ForeignKey(
        Project, related_name="external_defense_gradings", on_delete=models.CASCADE)
    
    problem_statement = models.IntegerField()
    project_methodology = models.IntegerField()
    result_discussion = models.IntegerField()
    conclusion = models.IntegerField()
    communication_skills = models.IntegerField()
    total = models.IntegerField()
    
    evaluator = models.ForeignKey(
        Staff, related_name="external_defense_grading_evaluations", on_delete=models.CASCADE)
    comment = models.TextField(null=True, blank=True)
    date_evaluated = models.DateField()
    signed = models.BooleanField()
    
    
    class Meta:
        verbose_name = "External Project Defense Grading"
        verbose_name_plural = "External Project Defense Grading"
        
    def __str__(self):
        return f"External Project Defense Grading for {self.project.title} by {self.evaluator}"
     
     

