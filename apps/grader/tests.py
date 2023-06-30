from django.test import TestCase
from .models import Staff, Student
from passlib.context import CryptContext

# Create your tests here.

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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
        


class StudentManagerTestCase(TestCase):
    
    def setUp(self):
        data = {
            "title":"First Project",
        }
        

    