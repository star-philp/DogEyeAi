import os
from pathlib import Path
import logging
import torch
import torchvision.transforms as transforms
from PIL import Image
import streamlit as st
from fastai.learner import load_learner

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define paths
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / 'models' / 'best_model.pkl'

# Define image transformation
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

def preprocess_image(image):
    """Preprocess the input image for model inference."""
    image = transform(image)
    image = image.unsqueeze(0)  # Add batch dimension
    return image

def load_model(model_path):
    """Load the pre-trained model."""
    try:
        learn = load_learner(model_path)
        logging.info("Model loaded successfully.")
        return learn
    except Exception as e:
        logging.error(f"An error occurred while loading the model: {e}")
        return None

def analyze_image(image, model):
    """Analyze the input image using the pre-trained model."""
    processed_image = preprocess_image(image)
    with torch.no_grad():
        pred_class, pred_idx, probs = model.predict(processed_image)
    return pred_class, pred_idx, probs

def main():
    # Load the model
    model = load_model(MODEL_PATH)
    if model is None:
        logging.error("Failed to load the model. Exiting...")
        return

    # Streamlit app
    st.title("Dog Eye Health Checker")

    # Upload Photo
    uploaded_file = st.file_uploader("Choose a file", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")  # Convert image to RGB
        st.image(image, caption='Uploaded Image', use_column_width=True)

        try:
            pred_class, pred_idx, probs = analyze_image(image, model)
            result_text = f"Analysis Output:\nClass: {pred_class}\nIndex: {pred_idx}\nProbabilities: {probs}"

            # Save results to DB
            # Note: Add your database saving logic here

            st.success("Analysis complete. Results have been saved.")
        except Exception as e:
            logging.error(f"An error occurred during analysis: {e}")
            st.error(f"An error occurred during analysis: {e}")

    # User Profile Page
    # Note: Add your logic for displaying stored results here

if __name__ == "__main__":
    main()
