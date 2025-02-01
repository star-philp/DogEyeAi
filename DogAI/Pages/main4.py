import torch  # torch를 임포트합니다.
import torchvision.transforms as transforms
from PIL import Image
import os
import streamlit as st
from fastai.learner import load_learner
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# Path to your model file
model_path = '/Users/rainstar/Project/Python/DogAI/models/best_model.pkl'

# Check if the model file exists
if not os.path.isfile(model_path):
    st.error(f"Model file not found at path: {model_path}")
    st.stop()

# Load the model using Fastai's load_learner function
try:
    learn = load_learner(model_path)  # Fastai's load_learner function for .pkl files
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
        # Use Fastai's predict function
        pred_class, pred_idx, probs = learn.predict(image)
    return pred_class, pred_idx, probs

def generate_heatmap(image):
    """
    Generate a heatmap from the model's output.
    This is a placeholder function. Replace it with actual heatmap generation logic.
    """
    # Create a random heatmap as a placeholder
    heatmap = np.random.random((224, 224))
    heatmap = cm.viridis(heatmap)  # Apply a colormap
    heatmap = (heatmap[..., :3] * 255).astype(np.uint8)  # Convert to RGB
    
    # Convert to PIL image
    return Image.fromarray(heatmap)

def overlay_heatmap_on_image(original_image, heatmap_image):
    """
    Overlay the heatmap on the original image.
    """
    original_image = original_image.resize(heatmap_image.size)  # Ensure sizes match
    original_array = np.array(original_image)
    heatmap_array = np.array(heatmap_image)
    
    # Combine the images
    combined_array = np.clip(original_array + heatmap_array, 0, 255).astype(np.uint8)
    
    return Image.fromarray(combined_array)

def severity_text(prob):
    """
    Convert probability to severity level text.
    """
    # Convert probability to a severity scale from 1 to 10
    level = int(round(prob * 10))
    level = min(max(level, 1), 10)  # Ensure level is between 1 and 10
    
    # Define severity messages
    messages = {
        1: "Very Low Risk: Symptoms are minimal.",
        2: "Low Risk: Symptoms are mild.",
        3: "Moderate Risk: Symptoms are present but manageable.",
        4: "Somewhat High Risk: Symptoms are noticeable and should be monitored.",
        5: "High Risk: Symptoms are significant, consult a vet.",
        6: "Very High Risk: Symptoms are severe, immediate action is needed.",
        7: "Critical Risk: Symptoms are critical, seek urgent veterinary care.",
        8: "Extreme Risk: Symptoms are very severe, and immediate professional help is required.",
        9: "Severe and Dangerous: Immediate intervention is necessary.",
        10: "Critical and Life-threatening: Emergency care required immediately."
    }
    
    return messages.get(level, "Unknown risk level.")

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
sample_image_path = '/Users/rainstar/Project/Python/DogAI/dog_inflammation/dog-inflammation/Negative/D0_0a529f92-60a5-11ec-8402-0a7404972c70.jpg'  # Update this path with the actual path to your sample image
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
        
        # Generate and overlay the heatmap
        heatmap_image = generate_heatmap(image)
        combined_image = overlay_heatmap_on_image(image, heatmap_image)
        
        # Display the combined image
        st.image(combined_image, caption='Image with Heatmap Overlay', use_column_width=True)
        
        # Display all severity messages
        st.subheader("Severity Scale")
        for level in range(1, 11):
            st.write(f"{level}: {severity_text(level / 10)}")
        
        # Display the severity level of the analysis result once
        severity_message = severity_text(probs.max().item())
        st.write(f"This is what it says:\n{severity_message}")
        
        # Save results to DB (Placeholder)
        # Note: Add your database saving logic here

        st.success("Analysis complete. Results have been saved.")
    except Exception as e:
        st.error(f"An error occurred during analysis: {e}")

    # User Profile Page
    # Note: Add your logic for displaying stored results here
