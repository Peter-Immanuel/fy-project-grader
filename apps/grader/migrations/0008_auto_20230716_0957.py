# Generated by Django 3.2.15 on 2023-07-16 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grader', '0007_auto_20230714_2104'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='device_score',
            field=models.IntegerField(blank=True, help_text='This is the score given to the student device (Hardware/Software integration)', null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='supervisor_score',
            field=models.IntegerField(blank=True, help_text="This is the score given to a student's project by their supervisor", null=True),
        ),
    ]
