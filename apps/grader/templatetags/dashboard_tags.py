from django import template

register = template.Library()


@register.filter
def get_project_student(staff):
    return staff.projects.filter(completed=False).count()