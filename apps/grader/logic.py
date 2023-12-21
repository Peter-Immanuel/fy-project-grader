# This is a helper module that define useful logics within the application

from django.db import models

from .models import (
    Student,
    Project,
    ProjectProposalGrading,
    ProjectWorkProgress,
    InternalDefense,
    ExternalDefense
)



def compute_student_score(student: Student, grading_model: models.Model):
    student_scores = grading_model.objects.filter(student=student)
    
    if not student_scores.exists():
        return False
    
    average  = 0 
    for score in student_scores:
        average += score.total
        
    score = round(average/len(student_scores), 3)    
        
    if grading_model.__name__.lower() == "projectproposalgrading":
        student.proposal_score = score
    elif grading_model.__name__.lower() == "projectworkprogress":
        student.work_progress_score = score
    elif grading_model.__name__.lower() == "internaldefense":
        student.internal_defense_score = score
    elif grading_model.__name__.lower() == "externaldefense":
        student.external_defense_score = score
    elif grading_model.__name__.lower() == "productevaluation":
        student.hardware_software_score = score
        
    student.save()
            
            
        
    
    