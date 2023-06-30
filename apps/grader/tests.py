from django.test import TestCase
from passlib.context import CryptContext
from .models import (
    Staff, Student,
    Faculty,Department,
    FinalYearSession,
    Project
)
from django.contrib.auth import get_user_model



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
User = get_user_model()

class StaffManagerTestCase(TestCase):
    
    def setUp(self):
        self.model = Staff
        self.data = {
            "email":"staff@st.futminna.edu.ng",
            "password":"staff001",
            "title":"Prof",
            "first_name":"B",
            "middle_name":"K",
            "last_name":"Nuhu",
            "staff_type":"Supervisor",
            "gender":"Male",
            "secret":"Secret"
        }
        
    def test_create_staff_profile(self):
        
        staff = Staff.objects.create_staff_profile(
            password=self.data.pop("password"),
            **self.data
        )
        self.assertTrue(staff.active)
        self.assertNotEqual(staff.secret, self.data.get("secret"))
        self.assertTrue(
            pwd_context.verify(self.data.get("secret"), staff.secret))
        
        self.assertTrue(User.objects.filter(email=staff.email).exists())

class StudentManagerTestCase(TestCase):
    
    def setUp(self):
        
        #Faculty, Department and Session Setup
        faculty = Faculty.objects.create(
            name="School of Electrical and Electronics Engineering",
            short_name = "SEET"
        )
        
        department = Department.objects.create(
            name="Computer Engineering Engineering",
            short_name = "CPE",
            faculty=faculty
        )
        
        session = FinalYearSession.objects.create(
            year="2023/2024")

        
        # Setup Supervisor
        staff_data = {
            "email":"staff@st.futminna.edu.ng",
            "password":"staff001",
            "title":"Prof",
            "first_name":"B",
            "middle_name":"K",
            "last_name":"Nuhu",
            "staff_type":"Supervisor",
            "gender":"Male",
            "secret":"Secret"
        }
        self.supervisor = Staff.objects.create_staff_profile(
            password=staff_data.pop("password"),
            **staff_data
        )
        
        self.data = {
            "first_name":"Bemshima",
            "middle_name":"Emmanuel",
            "last_name":"Peter",
            "email":"peter.m1701871@st.futminna.edu.ng",
            "matric_number":"2017/1/66491CP",
            "gender":"Male",
            "session":session,
            "department":department,
            "faculty":faculty, 
            "supervisor": self.supervisor,
            "title": "Sample Project Topic"
        }
        
        
    def test_create_student_details(self):
        student = Student.objects.create_student_details(
            # title=self.data.pop("title"),
            # supervisor=self.data.pop("supervisor"),
            **self.data
        )
        
        
        self.assertTrue(
            Student.objects.filter(
                matric_number=self.data.get("matric_number")).exists())
        
        self.assertTrue(
            Project.objects.filter(
                title=self.data.get("title")).exists()
        )
    