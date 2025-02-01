import torch
import torchvision.transforms as transforms
from PIL import Image
import os
import streamlit as st
from fastai.learner import load_learner

# Path to your model file
model_path = '/Users/rainstar/Project/Python/DogAI/models/best_model.pkl'

# Check if the model file exists
if not os.path.isfile(model_path):
    st.error(f"Model file not found at path: {model_path}")
    st.stop()

# Load the model
try:
    learn = load_learner(model_path)  # Using Fastai's load_learner function
    st.success("Model loaded successfully.")
except Exception as e:
    st.error(f"An error occurred while loading the model: {e}")
    st.stop()

# Define image transformation
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

def preprocess_image(image):
    image = transform(image)
    image = image.unsqueeze(0)  # Add batch dimension
    return image

def analyze_image(image):
    processed_image = preprocess_image(image)
    with torch.no_grad():
        # Use Fastai's prediction function
        pred_class, pred_idx, probs = learn.predict(image)
    return pred_class, pred_idx, probs

# Streamlit app
st.title("Dog Eye Health Checker")

# Upload Photo
uploaded_file = st.file_uploader("Choose a file", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")  # Convert image to RGB
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # Analyze Image
    try:
        pred_class, pred_idx, probs = analyze_image(image)
        result_text = f"Analysis Output:\nClass: {pred_class}\nIndex: {pred_idx}\nProbabilities: {probs}"
        
        # Display results in a text box
        st.text_area("Analysis Results", result_text, height=150)
        
        # Display the uploaded image again with the analysis result
        st.image(image, caption=f'Analysis Result: {pred_class}', use_column_width=True)
        
        # Save results to DB (Placeholder)
        # Note: Add your database saving logic here

        st.success("Analysis complete. Results have been saved.")
    except Exception as e:
        st.error(f"An error occurred during analysis: {e}")

    # User Profile Page
    # Note: Add your logic for displaying stored results here
