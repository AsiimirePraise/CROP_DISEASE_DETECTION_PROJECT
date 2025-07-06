
import time
import random
from celery import shared_task
from django.utils import timezone
from .models import DiagnosisRequest, DiagnosisResult, Disease, DiseaseDetection


@shared_task
def process_diagnosis(diagnosis_id):
    """
    Process crop disease diagnosis using AI/ML models.
    This is a placeholder implementation that simulates the processing.
    """
    try:
        diagnosis = DiagnosisRequest.objects.get(id=diagnosis_id)
        diagnosis.status = 'processing'
        diagnosis.save()
        
        start_time = time.time()
        
        # Simulate processing time
        time.sleep(random.uniform(2, 5))
        
        # Mock AI/ML processing results
        mock_results = [
            {'disease_name': 'Leaf Spot', 'confidence': 0.85, 'severity': 'medium'},
            {'disease_name': 'Rust Disease', 'confidence': 0.72, 'severity': 'low'},
            {'disease_name': 'Bacterial Wilt', 'confidence': 0.45, 'severity': 'high'},
        ]
        
        # Create diagnosis result
        result = DiagnosisResult.objects.create(
            diagnosis_request=diagnosis,
            overall_health_status='Needs Attention',
            recommendations='Apply appropriate fungicide treatment. Monitor closely for spread.',
            urgency_level='medium'
        )
        
        # Create disease detections
        for mock_result in mock_results:
            if mock_result['confidence'] > 0.5:  # Only include high confidence results
                try:
                    disease = Disease.objects.get(name=mock_result['disease_name'])
                    DiseaseDetection.objects.create(
                        diagnosis_result=result,
                        disease=disease,
                        confidence_score=mock_result['confidence'] * 100,
                        severity_assessment=mock_result['severity'],
                        affected_area_percentage=random.uniform(10, 60)
                    )
                except Disease.DoesNotExist:
                    # Create disease if it doesn't exist
                    disease = Disease.objects.create(
                        name=mock_result['disease_name'],
                        severity=mock_result['severity'],
                        symptoms='Symptoms to be updated',
                        treatment_methods='Treatment methods to be updated'
                    )
                    disease.crops.add(diagnosis.crop)
                    
                    DiseaseDetection.objects.create(
                        diagnosis_result=result,
                        disease=disease,
                        confidence_score=mock_result['confidence'] * 100,
                        severity_assessment=mock_result['severity'],
                        affected_area_percentage=random.uniform(10, 60)
                    )
        
        # Update diagnosis request
        processing_time = time.time() - start_time
        diagnosis.status = 'completed'
        diagnosis.confidence_score = max([r['confidence'] for r in mock_results]) * 100
        diagnosis.processing_time = processing_time
        diagnosis.save()
        
        return f"Diagnosis {diagnosis_id} processed successfully"
        
    except DiagnosisRequest.DoesNotExist:
        return f"Diagnosis {diagnosis_id} not found"
    except Exception as e:
        # Update status to failed
        try:
            diagnosis = DiagnosisRequest.objects.get(id=diagnosis_id)
            diagnosis.status = 'failed'
            diagnosis.save()
        except:
            pass
        return f"Error processing diagnosis {diagnosis_id}: {str(e)}"
