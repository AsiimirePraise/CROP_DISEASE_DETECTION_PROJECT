# Generated by Django 4.2.7 on 2025-07-16 15:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TrainingImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='training_images/')),
                ('label', models.CharField(max_length=255)),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
                ('verified', models.BooleanField(default=False)),
                ('uploaded_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FarmerUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='farmer_uploads/')),
                ('predicted_class', models.CharField(max_length=255)),
                ('confidence', models.FloatField()),
                ('crop_type', models.CharField(max_length=100)),
                ('disease', models.CharField(max_length=100)),
                ('severity', models.CharField(choices=[('None', 'None'), ('Low', 'Low'), ('Moderate', 'Moderate'), ('High', 'High'), ('Very High', 'Very High')], max_length=20)),
                ('primary_affected_part', models.CharField(max_length=100)),
                ('affected_parts', models.JSONField(default=list)),
                ('description', models.TextField()),
                ('symptoms', models.TextField()),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
                ('verified', models.BooleanField(default=False)),
                ('correct_prediction', models.BooleanField(blank=True, null=True)),
                ('admin_notes', models.TextField(blank=True, null=True)),
                ('farmer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
