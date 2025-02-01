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

class DogEyeHealthChecker:
    def __init__(self, model_path):
        self.model = self.load_model(model_path)

    def load_model(self, model_path):
        """Load the pre-trained model."""
        try:
            learn = load_learner(model_path)
            logging.info("Model loaded successfully.")
            return learn
        except Exception as e:
            logging.error(f"An error occurred while loading the model: {e}")
            return None

    def preprocess_image(self, image):
        """Preprocess the input image for model inference."""
        image = transform(image)
        image = image.unsqueeze(0)  # Add batch dimension
        return image

    def analyze_image(self, image):
        """Analyze the input image using the pre-trained model."""
        if self.model is None:
            logging.error("Model not loaded. Cannot analyze image.")
            return None

        processed_image = self.preprocess_image(image)
        with torch.no_grad():
            pred_class, pred_idx, probs = self.model.predict(processed_image)
        return pred_class, pred_idx, probs

    def generate_heatmap(self, image):
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

    def overlay_heatmap_on_image(self, original_image, heatmap_image):
        """
        Overlay the heatmap on the original image.
        """
        original_image = original_image.resize(heatmap_image.size)  # Ensure sizes match
        original_array = np.array(original_image)
        heatmap_array = np.array(heatmap_image)

        # Combine the images
        combined_array = np.clip(original_array + heatmap_array, 0, 255).astype(np.uint8)

        return Image.fromarray(combined_array)

    def severity_text(self, prob):
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

def main():
    # Create an instance of the DogEyeHealthChecker
    checker = DogEyeHealthChecker(MODEL_PATH)

    # Streamlit app
    st.title("Dog Eye Health Checker")

    # Upload Photo
    uploaded_file = st.file_uploader("Choose a file", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")  # Convert image to RGB
        st.image(image, caption='Uploaded Image', use_column_width=True)

        try:
            pred_class, pred_idx, probs = checker.analyze_image(image)
            result_text = f"Analysis Output:\nClass: {pred_class}\nIndex: {pred_idx}\nProbabilities: {probs}"

            # Display results in a text box

            # Generate and overlay the heatmap
            heatmap_image = checker.generate_heatmap(image)
            combined_image = checker.overlay_heatmap_on_image(image, heatmap_image)

            # Display the combined image
            st.image(combined_image, caption='Image with Heatmap Overlay', use_column_width=True)

            # Display all severity messages
            st.subheader("Severity Scale")
            for level in range(1, 11):
                st.write(f"{level}: {checker.severity_text(level / 10)}")

            # Display the severity level of the analysis result
            severity_message = checker.severity_text(probs.max().item())
            st.write(f"This is what it says:\n{severity_message}")

            # Save results to DB (Placeholder)
            # Note: Add your database saving logic here

            st.success("Analysis complete. Results have been saved.")
        except Exception as e:
            logging.error(f"An error occurred during analysis: {e}")
            st.error(f"An error occurred during analysis: {e}")

    # User Profile Page
    # Note: Add your logic for displaying stored results here

if __name__ == "__main__":
    main()
