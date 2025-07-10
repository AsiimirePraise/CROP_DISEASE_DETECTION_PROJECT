from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from keras.models import load_model
import numpy as np
from PIL import Image
import os
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Define class names mapping
class_names = {
    0: 'Apple___Apple_scab',
    1: 'Apple___Black_rot', 
    2: 'Apple___Cedar_apple_rust',
    3: 'Apple___healthy',
    4: 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
    5: 'Corn_(maize)___Common_rust_',
    6: 'Corn_(maize)___Northern_Leaf_Blight',
    7: 'Corn_(maize)___healthy',
    8: 'Pepper,_bell___Bacterial_spot',
    9: 'Pepper,_bell___healthy',
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

def load_model_once():
    global model
    if model is None:
        try:
            if os.path.exists(MODEL_PATH):
                print(f"Loading model from: {MODEL_PATH}")
                model = load_model(MODEL_PATH)
                print(f"Model loaded successfully from: {MODEL_PATH}")
                logger.info(f"Model loaded successfully from: {MODEL_PATH}")
                return model
            else:
                print(f"Model file not found at: {MODEL_PATH}")
                logger.error(f"Model file not found at: {MODEL_PATH}")
                return None
        except Exception as e:
            print(f"Error loading model from {MODEL_PATH}: {str(e)}")
            logger.error(f"Error loading model from {MODEL_PATH}: {str(e)}")
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
        'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot': {
            'crop': 'Corn',
            'disease': 'Gray Leaf Spot',
            'severity': 'High',
            'description': 'Fungal disease causing rectangular gray lesions on leaves'
        },
        'Corn_(maize)___Common_rust_': {
            'crop': 'Corn',
            'disease': 'Common Rust',
            'severity': 'Moderate',
            'description': 'Fungal disease causing rust-colored pustules on leaves'
        },
        'Corn_(maize)___Northern_Leaf_Blight': {
            'crop': 'Corn',
            'disease': 'Northern Leaf Blight',
            'severity': 'High',
            'description': 'Fungal disease causing large, cigar-shaped lesions on leaves'
        },
        'Corn_(maize)___healthy': {
            'crop': 'Corn',
            'disease': 'Healthy',
            'severity': 'None',
            'description': 'Plant appears healthy with no visible disease symptoms'
        },
        'Pepper,_bell___Bacterial_spot': {
            'crop': 'Bell Pepper',
            'disease': 'Bacterial Spot',
            'severity': 'High',
            'description': 'Bacterial disease causing dark spots on leaves and fruit'
        },
        'Pepper,_bell___healthy': {
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
            
            return HttpResponse(response_html)
            
        except Exception as e:
            logger.error(f"Error in prediction: {str(e)}")
            return HttpResponse(f"Error: An error occurred during prediction - {str(e)}", status=500)
    
    return render(request, 'index.html')
