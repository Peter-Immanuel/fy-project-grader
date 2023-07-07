# Generated by Django 3.2.15 on 2023-07-07 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grader', '0008_project_session'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='cordinator_approval',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='project',
            name='cordinator_comment',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='supervisor_approval',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='project',
            name='supervisor_comment',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='staff',
            name='staff_type',
            field=models.CharField(choices=[('Internal_Evaluator', 'Internal Evaluator'), ('External_Evaluator', 'External Evaluator'), ('Supervisor_and_Evaluator', 'Supervisor and Evaluator')], max_length=50),
        ),
    ]
