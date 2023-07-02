# Generated by Django 3.2.15 on 2023-07-02 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grader', '0006_alter_project_faculty'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='graduated',
            field=models.BooleanField(default=False, help_text='Indicates if the student has graduated or not'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='staff_type',
            field=models.CharField(choices=[('Supervisor', 'Supervisor'), ('Internal_Evaluator', 'Internal Evaluator'), ('External_Evaluator', 'External Evaluator'), ('Supervisor_and_Evaluator', 'Supervisor and Evaluator')], max_length=50),
        ),
    ]
