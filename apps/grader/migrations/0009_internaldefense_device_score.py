# Generated by Django 3.2.15 on 2023-07-16 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grader', '0008_auto_20230716_0957'),
    ]

    operations = [
        migrations.AddField(
            model_name='internaldefense',
            name='device_score',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]