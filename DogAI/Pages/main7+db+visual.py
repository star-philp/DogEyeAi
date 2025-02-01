import streamlit as st
import torch
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
import os
from fastai.learner import load_learner
import pandas as pd
from db_handler import connect_to_db, create_table_if_not_exists, save_results_to_db, load_data, close_db_connection
import matplotlib.cm as cm  # Importing colormap

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
    # Create a random heatmap as a placeholder
    heatmap = np.random.random((224, 224))
    heatmap = (cm.viridis(heatmap)[..., :3] * 255).astype(np.uint8)
    return Image.fromarray(heatmap)

def overlay_heatmap_on_image(original_image, heatmap_image):
    original_image = original_image.resize(heatmap_image.size)
    combined_array = np.clip(np.array(original_image) + np.array(heatmap_image), 0, 255).astype(np.uint8)
    return Image.fromarray(combined_array)

def severity_text(prob):
    level = int(round(prob * 10))
    level = min(max(level, 1), 10)
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
sample_image_path = 'path/to/your/sample_image.jpg'
if os.path.isfile(sample_image_path):
    sample_image = Image.open(sample_image_path)
    st.image(sample_image, caption='Sample Image: Follow these guidelines to capture a good photo.', use_column_width=True)
else:
    st.error(f"Sample image not found at path: {sample_image_path}")

# Upload Photo
uploaded_file = st.file_uploader("Choose a file", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption='Uploaded Image', use_column_width=True)

    conn = None  # conn을 초기화합니다.

    try:
        # Analyze Image
        pred_class, pred_idx, probs = analyze_image(image)
        result_text = f"Analysis Output:\nClass: {pred_class}\nIndex: {pred_idx}\nProbabilities: {probs}"
        st.text_area("Analysis Results", result_text, height=150)

        # Generate and overlay the heatmap
        heatmap_image = generate_heatmap(image)
        combined_image = overlay_heatmap_on_image(image, heatmap_image)
        st.image(combined_image, caption='Image with Heatmap Overlay', use_column_width=True)

        # Display all severity messages
        st.subheader("Severity Scale")
        for level in range(1, 11):
            st.write(f"{level}: {severity_text(level / 10)}")

        severity_message = severity_text(probs.max().item())
        st.write(f"This is what it says:\n{severity_message}")

        # Save results to PostgreSQL database
        conn = connect_to_db()
        create_table_if_not_exists(conn)
        save_results_to_db(conn, pred_class, pred_idx, probs)
        st.success("Analysis complete. Results have been saved to PostgreSQL database.")
    except Exception as e:
        st.error(f"An error occurred during analysis: {e}")
    finally:
        if conn:
            close_db_connection(conn)

    # Display saved results from the database
    # Display saved results from the database
    st.subheader("Previously Saved Results")
    data = load_data()
    if data is not None:
        st.dataframe(data)
    
    # Class distribution visualization
        st.subheader("Class Distribution")
        class_distribution = data['class'].value_counts().reset_index()
        class_distribution.columns = ['Class', 'Count']
        st.bar_chart(class_distribution)

    # Analysis over time visualization
        st.subheader("Analysis Over Time")  # Corrected line
        data['analysis_time'] = pd.to_datetime(data['analysis_time'])
        time_series = data.set_index('analysis_time').resample('D').size().reset_index()
        time_series.columns = ['Date', 'Count']
        st.line_chart(time_series)
    else:
        st.write("No data available.")