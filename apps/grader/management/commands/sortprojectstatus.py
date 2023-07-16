from typing import Any, Optional
from django.core.management import BaseCommand, CommandError
from ...models import Project




class Command(BaseCommand):
    help = "This command sorts previous project status"
    
    def handle(self, *args: Any, **options: Any):
        
        projects = Project.objects.filter(
            completed=False, supervisor_approval=True, supervisor_approval_status="Pending")
        
        for project in projects:
            if project.supervisor_approval:
                project.supervisor_approval_status = "Approved"
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully updated  {project.title}')
                )
            if project.cordinator_approval:
                if project.cordinator_approval_status == "Approved":
                    pass
                else:
                    project.cordinator_approval_status = "Approved"
                    
            project.save()
            
        
        