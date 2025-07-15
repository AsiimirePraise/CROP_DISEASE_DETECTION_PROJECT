from django.db import migrations, models
import django.db.models.deletion

def convert_uuids_to_bigints(apps, schema_editor):
    DiagnosisRequest = apps.get_model('diagnosis', 'DiagnosisRequest')
    for obj in DiagnosisRequest.objects.all():
        # Create a mapping from UUID to integer (using hash or other conversion)
        obj.temp_id = abs(hash(obj.id)) % (2**63)  # Ensure it fits in BigInt
        obj.save()

class Migration(migrations.Migration):
    dependencies = [
        ('diagnosis', '0001_initial'),  # Adjust to your actual dependency
    ]

    operations = [
        # Step 1: Add temporary BigInt field
        migrations.AddField(
            model_name='diagnosisrequest',
            name='temp_id',
            field=models.BigIntegerField(null=True),
        ),
        
        # Step 2: Convert data
        migrations.RunPython(convert_uuids_to_bigints),
        
        # Step 3: Remove original UUID field
        migrations.RemoveField(
            model_name='diagnosisrequest',
            name='id',
        ),
        
        # Step 4: Rename temp field to id and make primary
        migrations.RenameField(
            model_name='diagnosisrequest',
            old_name='temp_id',
            new_name='id',
        ),
        
        # Step 5: Set as primary key
        migrations.AlterField(
            model_name='diagnosisrequest',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]