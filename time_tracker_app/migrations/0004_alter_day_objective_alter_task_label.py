# Generated by Django 4.2.16 on 2024-10-09 14:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('time_tracker_app', '0003_task_label'),
    ]

    operations = [
        migrations.AlterField(
            model_name='day',
            name='objective',
            field=models.IntegerField(default=26280),
        ),
        migrations.AlterField(
            model_name='task',
            name='label',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='time_tracker_app.label'),
        ),
    ]
