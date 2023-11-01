from typing import Any
from django.core.management import BaseCommand
from ...models import ProjectProposalGrading, Student
from ...logic import compute_student_score
import logging




class Command(BaseCommand):
    help = "This command computes score for students"
    
    def handle(self, *args: Any, **options: Any):
        
        students = Student.objects.filter(active=True)
        for student in students:
            if not student.proposal_score:
                print(f"INFO: Computing Score for {student.get_full_name()}")
                compute_student_score(student, ProjectProposalGrading)
        print("INFO: Score computatio Successful")
            
        
        