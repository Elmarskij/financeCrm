# Generated by Django 3.1.2 on 2020-11-30 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_auto_20201130_2315'),
    ]

    operations = [
        migrations.AddField(
            model_name='bankaccount',
            name='deleted_on',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]