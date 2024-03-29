# Generated by Django 3.2.15 on 2023-07-08 12:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=500)),
                ('short_name', models.CharField(max_length=50)),
                ('inauguration_date', models.DateField(blank=True, null=True)),
                ('active', models.BooleanField(default=True, help_text='Indicates if the department still exisits or not')),
            ],
            options={
                'verbose_name': 'Department',
                'verbose_name_plural': 'Departments',
            },
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=500)),
                ('short_name', models.CharField(max_length=50)),
                ('inauguration_date', models.DateField(blank=True, null=True)),
                ('active', models.BooleanField(default=True, help_text='Indicates if the faculty still exisits or not')),
            ],
            options={
                'verbose_name': 'Faculty',
                'verbose_name_plural': 'Faculties',
            },
        ),
        migrations.CreateModel(
            name='FinalYearSession',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('year', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Final Year Session',
                'verbose_name_plural': 'Final Year Sessions',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.TextField()),
                ('aims', models.TextField(blank=True, null=True)),
                ('objectives', models.TextField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('proposal_score', models.IntegerField(blank=True, help_text='This is the average of 3 proposal grading scores', null=True)),
                ('work_progress_score', models.IntegerField(blank=True, help_text='This is the average of 3 project work progress scores', null=True)),
                ('internal_defense_score', models.IntegerField(blank=True, help_text='This is the average of 3 internal defense scores', null=True)),
                ('external_defense_score', models.IntegerField(blank=True, help_text='This is the average of 3 internal defense scores', null=True)),
                ('project_score', models.IntegerField(blank=True, help_text='This is the Average score of all 4 scores category', null=True)),
                ('supervisor_comment', models.TextField(blank=True, null=True)),
                ('supervisor_approval', models.BooleanField(default=False)),
                ('cordinator_comment', models.TextField(blank=True, null=True)),
                ('cordinator_approval', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('first_name', models.CharField(max_length=100)),
                ('middle_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('matric_number', models.CharField(max_length=100, unique=True)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')], max_length=20)),
                ('active', models.BooleanField(default=True, help_text='Indicates if the student is available or not (E.g a case where they leave the country or dies)')),
                ('graduated', models.BooleanField(default=False, help_text='Indicates if the student has graduated or not')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students', to='grader.department')),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students', to='grader.faculty')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students', to='grader.finalyearsession')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(choices=[('Prof', 'Prof'), ('Assitant Prof', 'Assitant Prof'), ('Dr', 'Dr'), ('Engr', 'Engr'), ('Mr', 'Mr'), ('Mrs', 'Mrs')], max_length=50)),
                ('first_name', models.CharField(max_length=100)),
                ('middle_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('staff_type', models.CharField(choices=[('Internal_Evaluator', 'Internal Evaluator'), ('External_Evaluator', 'External Evaluator'), ('Supervisor_and_Evaluator', 'Supervisor and Evaluator')], max_length=50)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')], max_length=20)),
                ('signature', models.FileField(upload_to='staff/signatures')),
                ('active', models.BooleanField(default=True, help_text='Indicates if the staff is available or not (E.g a case where they leave the country or dies)')),
                ('secret', models.TextField(help_text='Text used to validate the use of signature')),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='staffs', to='grader.department')),
                ('faculty', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='staffs', to='grader.faculty')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProjectWorkProgress',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('project_methodology', models.IntegerField()),
                ('preliminary_result', models.IntegerField()),
                ('communication_skills', models.IntegerField()),
                ('total', models.IntegerField()),
                ('comment', models.TextField(blank=True, null=True)),
                ('date_evaluated', models.DateField()),
                ('signed', models.BooleanField()),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_work_progress_gradings', to='grader.department')),
                ('evaluator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_work_progress_grading_evaluations', to='grader.staff')),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_work_progress_gradings', to='grader.faculty')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_work_progress_gradings', to='grader.project')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_work_progress_gradings', to='grader.finalyearsession')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_work_progress_gradings', to='grader.student')),
            ],
            options={
                'verbose_name': 'Project Work Progress Grading',
                'verbose_name_plural': 'Project Work Progress Gradings',
            },
        ),
        migrations.CreateModel(
            name='ProjectProposalGrading',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('objective_scope', models.IntegerField()),
                ('research_methodology', models.IntegerField()),
                ('literature_review', models.IntegerField()),
                ('communication_skills', models.IntegerField()),
                ('total', models.IntegerField()),
                ('comment', models.TextField(blank=True, null=True)),
                ('date_evaluated', models.DateField()),
                ('signed', models.BooleanField()),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_proposal_gradings', to='grader.department')),
                ('evaluator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_proposal_grading_evaluations', to='grader.staff')),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_proposal_gradings', to='grader.faculty')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_proposal_gradings', to='grader.project')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_proposal_gradings', to='grader.finalyearsession')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_proposal_gradings', to='grader.student')),
            ],
            options={
                'verbose_name': 'Project Proposal Grading',
                'verbose_name_plural': 'Project Proposal Gradings',
            },
        ),
        migrations.AddField(
            model_name='project',
            name='co_supervisor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='co_supervisor_students', to='grader.staff'),
        ),
        migrations.AddField(
            model_name='project',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='department_projects', to='grader.department'),
        ),
        migrations.AddField(
            model_name='project',
            name='faculty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='faculty_projects', to='grader.faculty'),
        ),
        migrations.AddField(
            model_name='project',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='grader.finalyearsession'),
        ),
        migrations.AddField(
            model_name='project',
            name='student',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='project', to='grader.student'),
        ),
        migrations.AddField(
            model_name='project',
            name='supervisor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='supervisor_students', to='grader.staff'),
        ),
        migrations.CreateModel(
            name='InternalDefense',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('problem_statement', models.IntegerField()),
                ('project_methodology', models.IntegerField()),
                ('result_discussion', models.IntegerField()),
                ('conclusion', models.IntegerField()),
                ('communication_skills', models.IntegerField()),
                ('total', models.IntegerField()),
                ('comment', models.TextField(blank=True, null=True)),
                ('date_evaluated', models.DateField()),
                ('signed', models.BooleanField()),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='internal_defense_gradings', to='grader.department')),
                ('evaluator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='internal_defense_grading_evaluations', to='grader.staff')),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='internal_defense_gradings', to='grader.faculty')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='internal_defense_gradings', to='grader.project')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='internal_defense_gradings', to='grader.finalyearsession')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='internal_defense_gradings', to='grader.student')),
            ],
            options={
                'verbose_name': 'Internal Project Defense Grading',
                'verbose_name_plural': 'Internal Project Defense Grading',
            },
        ),
        migrations.CreateModel(
            name='ExternalDefense',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('problem_statement', models.IntegerField()),
                ('project_methodology', models.IntegerField()),
                ('result_discussion', models.IntegerField()),
                ('conclusion', models.IntegerField()),
                ('communication_skills', models.IntegerField()),
                ('total', models.IntegerField()),
                ('comment', models.TextField(blank=True, null=True)),
                ('date_evaluated', models.DateField()),
                ('signed', models.BooleanField()),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='external_defense_gradings', to='grader.department')),
                ('evaluator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='external_defense_grading_evaluations', to='grader.staff')),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='external_defense_gradings', to='grader.faculty')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='external_defense_gradings', to='grader.project')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='external_defense_gradings', to='grader.finalyearsession')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='external_defense_gradings', to='grader.student')),
            ],
            options={
                'verbose_name': 'External Project Defense Grading',
                'verbose_name_plural': 'External Project Defense Grading',
            },
        ),
        migrations.AddField(
            model_name='department',
            name='cordinator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='deparment_cordinator', to='grader.staff'),
        ),
        migrations.AddField(
            model_name='department',
            name='faculty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='faculties', to='grader.faculty'),
        ),
    ]
