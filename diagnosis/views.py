from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from tensorflow.keras.models import load_model            # type: ignore
from tensorflow.keras.layers import InputLayer, Conv2D # type: ignore
from tensorflow.keras import regularizers, initializers # type: ignore
from tensorflow.keras.utils import custom_object_scope # type: ignore
import tensorflow as tf
import numpy as np
from PIL import Image
import os
import logging
from keras.layers import InputLayer 
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage


# Configure logging
logger = logging.getLogger(__name__)

# Define class names mapping
class_names = {
    0: 'Apple___Apple_scab',
    1: 'Apple___Black_rot', 
    2: 'Apple___Cedar_apple_rust',
    3: 'Apple___healthy',
    4: 'Corn_(maize)_Cercospora_leaf_spot Gray_leaf_spot',
    5: 'Corn_(maize)Common_rust',
    6: 'Corn_(maize)_Northern_Leaf_Blight',
    7: 'Corn_(maize)_healthy',
    8: 'Pepper,bell__Bacterial_spot',
    9: 'Pepper,bell__healthy',
    10: 'Potato___Early_blight',
    11: 'Potato___Late_blight',
    12: 'Potato___healthy',
    13: 'Tomato___Bacterial_spot',
    14: 'Tomato___Early_blight',
    15: 'Tomato___Late_blight',
    16: 'Tomato___Leaf_Mold',
    17: 'Tomato___Septoria_leaf_spot',
    18: 'Tomato___Spider_mites Two-spotted_spider_mite',
    19: 'Tomato___Target_Spot',
    20: 'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
    21: 'Tomato___Tomato_mosaic_virus',
    22: 'Tomato___healthy'
}

# Load model once at module level to avoid reloading on each request
import django
from django.conf import settings

# MODEL_PATH = os.path.join(settings.BASE_DIR, 'Diagnosis', 'models', 'crop_disease_model.h5')
MODEL_PATH = os.path.join(settings.BASE_DIR, 'CNN', 'crop_disease_model.h5')
model = None


import os
import logging


def load_model_once():
    global model
    if model is None:
        try:
            if os.path.exists(MODEL_PATH):
                print(f"Loading model from: {MODEL_PATH}")

                # Define custom objects to handle serialization issues
                custom_objects = {
                    # Fix for InputLayer batch_shape issue
                    'InputLayer': lambda **config: InputLayer(
                        input_shape=config.get('batch_shape', (None, 150, 150, 3))[1:],
                        name=config.get('name', 'input_layer')
                    ),
                    # Ensure compatibility with TF 2.12.0 dtype policies
                    'DTypePolicy': tf.keras.mixed_precision.Policy,
                    # Add other custom layers if needed (e.g., custom activations)
                }

                with custom_object_scope(custom_objects):
                    model = load_model(MODEL_PATH, compile=False)
                    print("Model loaded successfully with TF 2.12.0 compatibility fixes")
                    return model

            else:
                error_msg = f"Model file not found at: {MODEL_PATH}"
                print(error_msg)
                logger.error(error_msg)
                return None

        except Exception as e:
            logger.error(f"Model loading failed: {str(e)}")
            
            # Fallback: Try loading weights only (if architecture is known)
            try:
                from tensorflow.keras.models import Sequential                        # type: ignore
                from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense # type: ignore

                # Rebuild model architecture (adjust based on your model)
                model = Sequential([
                    InputLayer(input_shape=(150, 150, 3)),
                    Conv2D(32, (3, 3), activation='relu'),
                    MaxPooling2D((2, 2)),
                    Flatten(),
                    Dense(len(class_names), activation='softmax')
                ])
                model.load_weights(MODEL_PATH)  # Load weights only
                print("Model loaded via architecture reconstruction")
                return model

            except Exception as fallback_error:
                logger.error(f"Fallback loading failed: {str(fallback_error)}")
                return None

    return model

def preprocess_image(image_file):
    """Preprocess the uploaded image for prediction"""
    try:
        # Open and convert image
        image = Image.open(image_file)
        # covert to RGB
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        #resize
        image = image.resize((150, 150))
        
        # Convert to numpy array and normalize
        image_array = np.array(image) / 255.0
        
        # Add batch dimension
        image_array = np.expand_dims(image_array, axis=0)
        
        return image_array
    except Exception as e:
        logger.error(f"Error preprocessing image: {str(e)}")
        return None

def get_disease_info(predicted_class):
    """Get detailed information about the predicted disease"""
    disease_info = {
        'Apple___Apple_scab': {
            'crop': 'Apple',
            'disease': 'Apple Scab',
            'severity': 'Moderate',
            'description': 'Fungal disease causing dark, scabby lesions on leaves and fruit'
        },
        'Apple___Black_rot': {
            'crop': 'Apple',
            'disease': 'Black Rot',
            'severity': 'High',
            'description': 'Serious fungal disease causing fruit rot and leaf spots'
        },
        'Apple___Cedar_apple_rust': {
            'crop': 'Apple',
            'disease': 'Cedar Apple Rust',
            'severity': 'Moderate',
            'description': 'Fungal disease causing orange spots on leaves'
        },
        'Apple___healthy': {
            'crop': 'Apple',
            'disease': 'Healthy',
            'severity': 'None',
            'description': 'Plant appears healthy with no visible disease symptoms'
        },
        'Corn_(maize)_Cercospora_leaf_spot Gray_leaf_spot': {
            'crop': 'Corn',
            'disease': 'Gray Leaf Spot',
            'severity': 'High',
            'description': 'Fungal disease causing rectangular gray lesions on leaves'
        },
        'Corn_(maize)Common_rust': {
            'crop': 'Corn',
            'disease': 'Common Rust',
            'severity': 'Moderate',
            'description': 'Fungal disease causing rust-colored pustules on leaves'
        },
        'Corn_(maize)_Northern_Leaf_Blight': {
            'crop': 'Corn',
            'disease': 'Northern Leaf Blight',
            'severity': 'High',
            'description': 'Fungal disease causing large, cigar-shaped lesions on leaves'
        },
        'Corn_(maize)_healthy': {
            'crop': 'Corn',
            'disease': 'Healthy',
            'severity': 'None',
            'description': 'Plant appears healthy with no visible disease symptoms'
        },
        'Pepper,bell__Bacterial_spot': {
            'crop': 'Bell Pepper',
            'disease': 'Bacterial Spot',
            'severity': 'High',
            'description': 'Bacterial disease causing dark spots on leaves and fruit'
        },
        'Pepper,bell__healthy': {
            'crop': 'Bell Pepper',
            'disease': 'Healthy',
            'severity': 'None',
            'description': 'Plant appears healthy with no visible disease symptoms'
        },
        'Potato___Early_blight': {
            'crop': 'Potato',
            'disease': 'Early Blight',
            'severity': 'High',
            'description': 'Fungal disease causing dark spots with concentric rings on leaves'
        },
        'Potato___Late_blight': {
            'crop': 'Potato',
            'disease': 'Late Blight',
            'severity': 'Very High',
            'description': 'Serious fungal disease that can destroy entire crops rapidly'
        },
        'Potato___healthy': {
            'crop': 'Potato',
            'disease': 'Healthy',
            'severity': 'None',
            'description': 'Plant appears healthy with no visible disease symptoms'
        },
        'Tomato___Bacterial_spot': {
            'crop': 'Tomato',
            'disease': 'Bacterial Spot',
            'severity': 'High',
            'description': 'Bacterial disease causing dark spots on leaves and fruit'
        },
        'Tomato___Early_blight': {
            'crop': 'Tomato',
            'disease': 'Early Blight',
            'severity': 'High',
            'description': 'Fungal disease causing dark spots with target-like patterns'
        },
        'Tomato___Late_blight': {
            'crop': 'Tomato',
            'disease': 'Late Blight',
            'severity': 'Very High',
            'description': 'Devastating fungal disease that can destroy crops quickly'
        },
        'Tomato___Leaf_Mold': {
            'crop': 'Tomato',
            'disease': 'Leaf Mold',
            'severity': 'Moderate',
            'description': 'Fungal disease causing yellow patches and fuzzy growth on leaves'
        },
        'Tomato___Septoria_leaf_spot': {
            'crop': 'Tomato',
            'disease': 'Septoria Leaf Spot',
            'severity': 'Moderate',
            'description': 'Fungal disease causing small, circular spots with dark borders'
        },
        'Tomato___Spider_mites Two-spotted_spider_mite': {
            'crop': 'Tomato',
            'disease': 'Spider Mites',
            'severity': 'Moderate',
            'description': 'Pest infestation causing stippled, yellowing leaves'
        },
        'Tomato___Target_Spot': {
            'crop': 'Tomato',
            'disease': 'Target Spot',
            'severity': 'Moderate',
            'description': 'Fungal disease causing circular spots with concentric rings'
        },
        'Tomato___Tomato_Yellow_Leaf_Curl_Virus': {
            'crop': 'Tomato',
            'disease': 'Yellow Leaf Curl Virus',
            'severity': 'High',
            'description': 'Viral disease causing yellowing and curling of leaves'
        },
        'Tomato___Tomato_mosaic_virus': {
            'crop': 'Tomato',
            'disease': 'Mosaic Virus',
            'severity': 'High',
            'description': 'Viral disease causing mottled, mosaic-like patterns on leaves'
        },
        'Tomato___healthy': {
            'crop': 'Tomato',
            'disease': 'Healthy',
            'severity': 'None',
            'description': 'Plant appears healthy with no visible disease symptoms'
        }
    }
    
    return disease_info.get(predicted_class, {
        'crop': 'Unknown',
        'disease': 'Unknown',
        'severity': 'Unknown',
        'description': 'Disease information not available'
    })

def index(request):
    if request.method == 'POST':
        try:
             # 1. Get the uploaded file
            uploaded_file = request.FILES['crop_image']
            
            # 2. Save the file to media folder
            from django.core.files.storage import FileSystemStorage
            fs = FileSystemStorage()
            filename = fs.save(f'uploaded_{uploaded_file.name}', uploaded_file)
            image_url = fs.url(filename)  # This defines image_url
            
            # Debug: Print all POST data and FILES
            print("POST data keys:", list(request.POST.keys()))
            print("FILES data keys:", list(request.FILES.keys()))
            print("Content type:", request.content_type)
            
            # Load model
            loaded_model = load_model_once()
            if loaded_model is None:
                return HttpResponse(f"Error: Model could not be loaded from {MODEL_PATH}. Please check if the file exists and has proper permissions.", status=500)
            
            # Check if image file is provided
            if 'crop_image' not in request.FILES:
                debug_info = f"Error: No image file provided.\n"
                debug_info += f"Available files: {list(request.FILES.keys())}\n"
                debug_info += f"POST data: {dict(request.POST)}\n"
                debug_info += f"Content type: {request.content_type}"
                return HttpResponse(debug_info, status=400)
            
            crop_image = request.FILES['crop_image']
            
            # Debug: Print file information
            print(f"File name: {crop_image.name}")
            print(f"File size: {crop_image.size}")
            print(f"File content type: {crop_image.content_type}")
            
            # Validate file type
            allowed_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
            file_extension = os.path.splitext(crop_image.name)[1].lower()
            if file_extension not in allowed_extensions:
                return HttpResponse("Error: Invalid file type. Please upload JPG, PNG, or BMP files.", status=400)
            
            # Preprocess the image
            processed_image = preprocess_image(crop_image)
            if processed_image is None:
                return HttpResponse("Error: Could not process the image", status=400)
            
            # Make prediction
            predictions = loaded_model.predict(processed_image)
            predicted_label = np.argmax(predictions[0])
            
            # Validate prediction index
            if predicted_label >= len(class_names):
                return HttpResponse(f"Error: Invalid prediction index {predicted_label}. Model predicted class outside expected range.", status=500)
            
            # Get the crop disease name
            predicted_crop = class_names.get(predicted_label, "Unknown")
            confidence = float(predictions[0][predicted_label]) * 100
            
            # Get detailed disease information
            disease_info = get_disease_info(predicted_crop)
            
            # Create detailed response
            response_html = f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2>Crop Disease Detection Result</h2>
                <div style="background-color: #f0f0f0; padding: 15px; border-radius: 5px; margin: 10px 0;">
                    <h3>Prediction: {predicted_crop}</h3>
                    <p><strong>Confidence:</strong> {confidence:.2f}%</p>
                </div>
                
                <div style="background-color: #e8f4f8; padding: 15px; border-radius: 5px; margin: 10px 0;">
                    <h4>Disease Information:</h4>
                    <p><strong>Crop:</strong> {disease_info['crop']}</p>
                    <p><strong>Disease:</strong> {disease_info['disease']}</p>
                    <p><strong>Severity:</strong> {disease_info['severity']}</p>
                    <p><strong>Description:</strong> {disease_info['description']}</p>
                </div>
                
                <div style="margin-top: 20px;">
                    <a href="/" style="background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
                        Upload Another Image
                    </a>
                </div>
            </div>
            """
            
        # For AJAX requests, return JSON
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'image_url': image_url,
                    'diagnosis': predicted_crop,
                    'confidence': confidence,
                    'description': disease_info['description'],
                    'treatment': get_treatment_advice(disease_info['disease']),
                    'crop': disease_info['crop'],
                    'severity': disease_info['severity']
                })
            else:
                # For regular form submission, return HTML
                return HttpResponse(response_html)

        except Exception as e:
            logger.error(f"Error: {str(e)}")
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': str(e)})
            return HttpResponse(f"Error: {str(e)}", status=500)
            
        except Exception as e:
            logger.error(f"Error in prediction: {str(e)}")
            return HttpResponse(f"Error: An error occurred during prediction - {str(e)}", status=500)
    
    return render(request, 'index.html')
@csrf_exempt
def upload(request):
    if request.method == 'POST' and request.FILES.get('crop_image'):
        try:
            # 1. Get the uploaded file
            uploaded_file = request.FILES['crop_image']
            
            # 2. Load the model
            loaded_model = load_model_once()
            if loaded_model is None:
                return JsonResponse({
                    'success': False,
                    'error': f"Model could not be loaded from {MODEL_PATH}"
                }, status=500)
            
            # 3. Validate file type
            allowed_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
            file_extension = os.path.splitext(uploaded_file.name)[1].lower()
            if file_extension not in allowed_extensions:
                return JsonResponse({
                    'success': False,
                    'error': "Invalid file type. Please upload JPG, PNG, or BMP files."
                }, status=400)
            
            # 4. Save the uploaded file to media folder
            from django.core.files.storage import FileSystemStorage
            fs = FileSystemStorage()
            filename = fs.save(f'uploaded_{uploaded_file.name}', uploaded_file)
            image_url = fs.url(filename)
            
            # 5. Preprocess the image
            processed_image = preprocess_image(uploaded_file)
            if processed_image is None:
                # Clean up the saved file if processing fails
                fs.delete(filename)
                return JsonResponse({
                    'success': False,
                    'error': "Could not process the image"
                }, status=400)
            
            # 6. Make prediction
            predictions = loaded_model.predict(processed_image)
            predicted_label = np.argmax(predictions[0])
            
            # 7. Validate prediction index
            if predicted_label >= len(class_names):
                fs.delete(filename)  # Clean up file if prediction fails
                return JsonResponse({
                    'success': False,
                    'error': f"Invalid prediction index {predicted_label}"
                }, status=500)
            
            # 8. Get prediction details
            predicted_crop = class_names.get(predicted_label, "Unknown")
            confidence = float(predictions[0][predicted_label]) * 100
            
            # 9. Get detailed disease information
            disease_info = get_disease_info(predicted_crop)
            
            # 10. Prepare response data
            response_data = {
                'success': True,
                'image_url': image_url,
                'diagnosis': disease_info['disease'],
                'confidence': round(confidence, 2),
                'description': disease_info['description'],
                'treatment': get_treatment_advice(disease_info['disease']),
                'crop': disease_info['crop'],
                'severity': disease_info['severity'],
                'timestamp': datetime.now().isoformat()
            }
            
            return JsonResponse(response_data)
            
        except Exception as e:
            # Clean up file if any exception occurs
            if 'filename' in locals():
                fs.delete(filename)
            logger.error(f"Error in upload/prediction: {str(e)}")
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method or no image provided'
    }, status=400)
    
def get_treatment_advice(disease):
    """Returns treatment advice based on disease type"""
    treatment_advice = {
        'Apple Scab': 'Apply fungicides containing myclobutanil or sulfur. Remove infected leaves and debris.',
        'Black Rot': 'Prune infected branches. Apply fungicides with captan or thiophanate-methyl.',
        'Cedar Apple Rust': 'Remove nearby junipers if possible. Apply fungicides in early spring.',
        'Gray Leaf Spot': 'Rotate crops. Apply fungicides with azoxystrobin or pyraclostrobin.',
        'Common Rust': 'Plant resistant varieties. Apply fungicides with propiconazole.',
        'Northern Leaf Blight': 'Use resistant hybrids. Apply fungicides early in season.',
        'Bacterial Spot': 'Use copper-based bactericides. Avoid overhead irrigation.',
        'Early Blight': 'Rotate crops. Apply chlorothalonil or copper-based fungicides.',
        'Late Blight': 'Destroy infected plants. Apply fungicides with mefenoxam.',
        'Leaf Mold': 'Improve air circulation. Apply chlorothalonil or copper fungicides.',
        'Septoria Leaf Spot': 'Remove infected leaves. Apply copper-based fungicides.',
        'Spider Mites': 'Use miticides or insecticidal soaps. Encourage natural predators.',
        'Target Spot': 'Apply fungicides with chlorothalonil. Remove plant debris.',
        'Yellow Leaf Curl Virus': 'Control whiteflies. Remove infected plants immediately.',
        'Mosaic Virus': 'Control aphids. Remove infected plants to prevent spread.',
        'Healthy': 'No treatment needed. Continue good cultural practices.'
    }
    return treatment_advice.get(disease, 'Consult with a local agricultural expert for specific treatment recommendations.')