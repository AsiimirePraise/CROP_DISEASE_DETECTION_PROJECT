from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse # type: ignore
from keras.models import load_model # type: ignore
import numpy as np
from PIL import Image
from django.conf import settings # type: ignore
import os
import logging
import json
import traceback
import base64 
from io import BytesIO 
from django.core.paginator import Paginator

from django.contrib import messages



from django.db import transaction
from .models import DiagnosisRequest, Disease, Crop, DiseasePrediction, ReportedIssue 
from django.core.files.uploadedfile import InMemoryUploadedFile
from .forms import ImageUploadForm
from django.contrib.auth.decorators import login_required


# Configure logging
logger = logging.getLogger(__name__)

class_names = {
    0: 'Tomato___Late_blight',
    1: 'Corn_(maize)___healthy',
    2: 'Pepper,_bell___Bacterial_spot',
    3: 'Tomato___Spider_mites Two-spotted_spider_mite',
    4: 'Tomato___Leaf_Mold',
    5: 'Corn_(maize)___Common_rust_',
    6: 'Potato___Early_blight',
    7: 'Apple___healthy',
    8: 'Tomato___Tomato_mosaic_virus',
    9: 'Potato___Late_blight',
    10: 'Pepper,_bell___healthy',
    11: 'Tomato___Target_Spot',
    12: 'Apple___Cedar_apple_rust',
    13: 'Apple___Black_rot',
    14: 'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
    15: 'Tomato___Bacterial_spot',
    16: 'Apple___Apple_scab',
    17: 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
    18: 'Tomato___Septoria_leaf_spot',
    19: 'Tomato___Early_blight',
    20: 'Corn_(maize)___Northern_Leaf_Blight',
    21: 'Potato___healthy',
    22: 'Tomato___healthy'
}

MODEL_PATH = os.path.join(settings.BASE_DIR, 'CNN', 'best_model.h5')
DISEASE_INFO_PATH =os.path.join(settings.BASE_DIR, 'disease_info.json') 
RECOMMENDATIONS_PATH =os.path.join(settings.BASE_DIR, 'recommendations.json')

model = None
disease_database = None
recommendations_database = None

def load_disease_info():
    """Load disease information from JSON file"""
    global disease_database
    if disease_database is None:
        try:
            if os.path.exists(DISEASE_INFO_PATH):
                with open(DISEASE_INFO_PATH, 'r', encoding='utf-8') as file:
                    disease_database = json.load(file)
                    logger.info(f"Disease database loaded successfully from: {DISEASE_INFO_PATH}")
            else:
                logger.error(f"Disease info file not found at: {DISEASE_INFO_PATH}")
                return None
        except Exception as e:
            logger.error(f"Error loading disease info from {DISEASE_INFO_PATH}: {str(e)}")
            return None
    return disease_database

def load_recommendations():
    """Load recommendations from JSON file"""
    global recommendations_database
    if recommendations_database is None:
        try:
            if os.path.exists(RECOMMENDATIONS_PATH):
                with open(RECOMMENDATIONS_PATH, 'r', encoding='utf-8') as file:
                    recommendations_database = json.load(file)
                    logger.info(f"Recommendations database loaded successfully from: {RECOMMENDATIONS_PATH}")
            else:
                logger.error(f"Recommendations file not found at: {RECOMMENDATIONS_PATH}")
                return None
        except Exception as e:
            logger.error(f"Error loading recommendations from {RECOMMENDATIONS_PATH}: {str(e)}")
            return None
    return recommendations_database

def load_model_once():
    """Load the Keras model once"""
    global model
    if model is None:
        try:
            if os.path.exists(MODEL_PATH):
                logger.info(f"Loading model from: {MODEL_PATH}")
                model = load_model(MODEL_PATH)
                logger.info(f"Model loaded successfully from: {MODEL_PATH}")
            else:
                logger.error(f"Model file not found at: {MODEL_PATH}")
                return None
        except Exception as e:
            logger.error(f"Error loading model from {MODEL_PATH}: {str(e)}")
            return None
    return model

def preprocess_image(image_file):
    """Preprocess the uploaded image for prediction and return image array and base64 string."""
    try:
        image = Image.open(image_file)
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Save original image to BytesIO for base64 encoding
        buffered = BytesIO()
        image.save(buffered, format="PNG") # Use PNG for better quality and transparency if needed
        img_str = base64.b64encode(buffered.getvalue()).decode()
        image_base64 = f"data:image/png;base64,{img_str}"

        # Resize for model prediction
        image = image.resize((224, 224))
        image_array = np.array(image) / 255.0
        image_array = np.expand_dims(image_array, axis=0)

        return image_array, image_base64
    except Exception as e:
        logger.error(f"Error preprocessing image: {str(e)}")
        return None, None

def get_severity_level(confidence, disease_name):
    """Determine severity level based on confidence and disease type"""
    if 'healthy' in disease_name.lower():
        return 'None'

    high_risk_diseases = ['Late_blight', 'Black_rot', 'Bacterial_spot', 'Northern_Leaf_Blight', 'Yellow_Leaf_Curl_Virus', 'Mosaic_virus']
    moderate_risk_diseases = ['Early_blight', 'Common_rust', 'Apple_scab', 'Cedar_apple_rust', 'Leaf_Mold', 'Septoria_leaf_spot', 'Target_Spot', 'Spider_mites']

    disease_type_high = any(risk.lower() in disease_name.lower() for risk in high_risk_diseases)
    disease_type_moderate = any(risk.lower() in disease_name.lower() for risk in moderate_risk_diseases)

    if disease_type_high:
        if confidence > 85:
            return 'Very High'
        elif confidence > 65:
            return 'High'
        else:
            return 'Moderate'
    elif disease_type_moderate:
        if confidence > 90:
            return 'High'
        elif confidence > 70:
            return 'Moderate'
        else:
            return 'Low'
    else: # For other diseases or less critical ones
        if confidence > 90:
            return 'High'
        elif confidence > 70:
            return 'Moderate'
        else:
            return 'Low'

def get_disease_info(predicted_class, confidence):
    """Get detailed information about the predicted disease from JSON file"""
    disease_db = load_disease_info()

    if disease_db is None:
        return {
            'crop': 'Unknown',
            'disease': 'Unknown',
            'affected_parts': ['Unknown'],
            'primary_affected': 'Unknown',
            'description': 'Disease information not available - JSON file could not be loaded',
            'symptoms': 'Unable to determine symptoms',
            'severity': get_severity_level(confidence, predicted_class)
        }

    info = disease_db.get(predicted_class, {
        'crop': 'Unknown',
        'disease': 'Unknown',
        'affected_parts': ['Unknown'],
        'primary_affected': 'Unknown',
        'description': 'Disease information not available in database',
        'symptoms': 'Unable to determine symptoms'
    })

    info['severity'] = get_severity_level(confidence, predicted_class)
    return info

def get_recommendations(predicted_class):
    """Get recommendations for the predicted disease from JSON file"""
    reco_db = load_recommendations()
    if reco_db is None:
        return ["Recommendations not available - JSON file could not be loaded."]
    return reco_db.get(predicted_class, ["No specific recommendations found for this disease."])

@login_required
def index(request):
    if request.method == 'POST':

          # Check if this is a report issue request
        if request.POST.get('action') == 'report_issue':
            return handle_report_issue(request)
        
        try:
            loaded_model = load_model_once()
            if loaded_model is None:
                return JsonResponse({"success": False, "error": f"Model could not be loaded from {MODEL_PATH}."}, status=500)

            disease_db = load_disease_info()
            if disease_db is None:
                return JsonResponse({"success": False, "error": f"Disease information could not be loaded from {DISEASE_INFO_PATH}."}, status=500)

            recommendations_db = load_recommendations()
            if recommendations_db is None:
                return JsonResponse({"success": False, "error": f"Recommendations could not be loaded from {RECOMMENDATIONS_PATH}."}, status=500)

            if 'crop_image' not in request.FILES:
                return JsonResponse({"success": False, "error": "No image file provided."}, status=400)

            crop_image = request.FILES['crop_image']
            allowed_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
            file_extension = os.path.splitext(crop_image.name)[1].lower()
            if file_extension not in allowed_extensions:
                return JsonResponse({"success": False, "error": "Invalid file type. Please upload JPG, PNG, or BMP files."}, status=400)
        except Exception as e:
            logger.error(f"Error in input validation: {traceback.format_exc()}")
            return JsonResponse({
                "success": False,
                "error": "Failed to validate input",
                "detail": str(e)
            }, status=500)

        loaded_model = load_model_once()
        if loaded_model is None:
            return JsonResponse({"success": False, "error": "Model could not be loaded."}, status=500)


        form = ImageUploadForm(request.POST, request.FILES, request=request)

        if not form.is_valid():
            return JsonResponse({
                "success": False,
                "error": form.errors.as_json()
            }, status=400)

        try:
            with transaction.atomic():
                diagnosis_request = form.save()  # Only save ONCE, and this sets the user too

                # Get the uploaded image
                crop_image = form.cleaned_data['image']
                processed_image_array, image_base64 = preprocess_image(crop_image)

                # Predict
                predictions = loaded_model.predict(processed_image_array)
                predicted_label = np.argmax(predictions[0])
                predicted_class_name = class_names.get(predicted_label, "Unknown")
                confidence = float(predictions[0][predicted_label]) * 100

                # Disease info & recommendations
                disease_info = get_disease_info(predicted_class_name, confidence)
                recommendations = get_recommendations(predicted_class_name)

                # Update diagnosis with results
                diagnosis_request.status = DiagnosisRequest.Status.COMPLETED
                diagnosis_request.confidence_score = confidence / 100
                diagnosis_request.severity = disease_info['severity']
                diagnosis_request.notes = f"Auto-detected as {predicted_class_name}"
                diagnosis_request.save()  # Save updated fields

                # Create prediction
                DiseasePrediction.objects.create(
                    user=request.user,
                    image=crop_image,
                    predicted_class=predicted_class_name,
                    confidence=confidence,
                    disease_info=disease_info,
                    recommendations=recommendations,
                    severity=disease_info['severity'],
                    diagnosis_request=diagnosis_request
                )

                return JsonResponse({
                    "success": True,
                    "image_url": image_base64,
                    "predicted_class_name": predicted_class_name,
                    "confidence": round(confidence, 2),
                    "disease_info": disease_info,
                    "recommendations": recommendations,
                    "diagnosis_id": diagnosis_request.id
                })

        except Exception as e:
            logger.error(f"Error in diagnosis: {traceback.format_exc()}")
            return JsonResponse({
                "success": False,
                "error": "Failed to process diagnosis",
                "detail": str(e)
            }, status=500)

    else:
        form = ImageUploadForm()
    return render(request, 'index.html', {'form': form})

def get_prediction_detail(request, prediction_id):
    """API endpoint to get prediction details"""
    try:
        prediction = DiseasePrediction.objects.get(id=prediction_id)
        data = {
            'id': prediction.id,
            'image_url': prediction.image.url if prediction.image else None,
            'predicted_class': prediction.predicted_class,
            'confidence': prediction.confidence,
            'disease_info': prediction.disease_info,
            'recommendations': prediction.recommendations,
            'created_at': prediction.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            'severity': prediction.severity
        }
        return JsonResponse({'success': True, 'data': data})
    
    except DiseasePrediction.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Prediction not found'}, status=404)
    
    from django.shortcuts import render
from django.core.paginator import Paginator
from .models import DiseasePrediction  # Make sure this model exists

def prediction_history(request):
    """View to display prediction history"""
    # Get all predictions ordered by most recent
    predictions = DiseasePrediction.objects.all().order_by('-created_at')
    
    # Add pagination (10 items per page)
    paginator = Paginator(predictions, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'diagnosis/prediction_history.html', {
        'page_obj': page_obj
    })

def reportIssue(request):
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        
        # Validation
        if not title or not description:
            error_message = 'Both title and description are required.'
            
            # Check if it's an AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': error_message
                })
            else:
                messages.error(request, error_message)
                return redirect('index')  # Redirect back to index page
        
        # Create the reported issue
        try:
            ReportedIssue.objects.create(
                user=request.user if request.user.is_authenticated else None,
                title=title,
                description=description
            )
            
            success_message = 'Your issue has been reported successfully!'
            
            # Check if it's an AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': success_message
                })
            else:
                messages.success(request, success_message)
                return redirect('index')  # Redirect back to index page
                
        except Exception as e:
            error_message = 'An error occurred while reporting the issue. Please try again.'
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': error_message
                })
            else:
                messages.error(request, error_message)
                return redirect('index')
    
    # If GET request, redirect to index page
    return redirect('index')

#def handle_report_issue(request):
    if request.method == 'POST' and request.POST.get('action') == 'report_issue':
        # Handle report issue functionality
        title = request.POST.get('title')
        description = request.POST.get('description')
        
        # Validation
        if not title or not description:
            error_message = 'Both title and description are required.'
            
            # Check if it's an AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': error_message
                })
            else:
                messages.error(request, error_message)
                return redirect('index')
        
        # Create the reported issue (THIS SAVES TO DATABASE)
        try:
            ReportedIssue.objects.create(
                user=request.user if request.user.is_authenticated else None,
                title=title,
                description=description
            )
            
            success_message = 'Your issue has been reported successfully!'
            
            # Check if it's an AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': success_message
                })
            else:
                messages.success(request, success_message)
                return redirect('index')
                
        except Exception as e:
            logger.exception("Error creating reported issue:")
            error_message = 'An error occurred while reporting the issue. Please try again.'
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': error_message
                })
            else:
                messages.error(request, error_message)
                return redirect('index')
    # If not POST or action not report_issue, redirect to index
    return redirect('index')