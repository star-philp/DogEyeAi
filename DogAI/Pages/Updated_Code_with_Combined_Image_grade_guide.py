import torch
import torchvision.transforms as transforms
from PIL import Image
import os
import streamlit as st
from fastai.learner import load_learner
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

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

# Display user tips
st.header("Guidelines for Taking Pictures")
st.write("""
1. **Lighting:** Ensure the image is well-lit. Natural light is best, but if indoors, use soft lighting to avoid harsh shadows.
2. **Focus:** Make sure the image is in focus. Blurry images can hinder accurate analysis.
3. **Background:** Use a plain background that contrasts with the subject to avoid distractions.
4. **Positioning:** Position the camera so that the subject is centered and fills most of the frame. Avoid too close or too far shots.
5. **Orientation:** Keep the image upright and ensure the subject is not tilted.
6. **Distance:** Maintain a consistent distance from the subject. Ensure the entire subject is visible in the image.
""")

# Display a sample image
st.subheader("Sample Image for Reference")
sample_image_path = '/Users/rainstar/Project/Python/DogAI/dog_inflammation/dog-inflammation/Negative/sample_image.jpg'  # Update this path with the actual path to your sample image
if os.path.isfile(sample_image_path):
    sample_image = Image.open(sample_image_path)
    st.image(sample_image, caption='Sample Image: Follow these guidelines to capture a good photo.', use_column_width=True)
else:
    st.error(f"Sample image not found at path: {sample_image_path}")

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

        # Display the heatmap
        st.write("Heatmap not available for this model.")

        # Save results to DB (Placeholder)
        # Note: Add your database saving logic here

        st.success("Analysis complete. Results have been saved.")
    except Exception as e:
        st.error(f"An error occurred during analysis: {e}")

    # User Profile Page
    # Note: Add your logic for displaying stored results here
