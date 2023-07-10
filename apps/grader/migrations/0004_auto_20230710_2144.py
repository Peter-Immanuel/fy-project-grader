# Generated by Django 3.2.15 on 2023-07-10 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grader', '0003_alter_staff_signature'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='staff',
            name='title',
            field=models.CharField(choices=[('Prof', 'Prof'), ('Associate Prof', 'Associate Prof'), ('Dr', 'Dr'), ('Engr', 'Engr'), ('Mr', 'Mr'), ('Mrs', 'Mrs')], max_length=50),
        ),
    ]
