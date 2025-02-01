from fastai.vision.all import *
from pathlib import Path
import matplotlib.pyplot as plt

EXTRACTED_FOLDER = Path('/Users/rainstar/Project/Python/DogAI/dog_inflammation')
#/Users/rainstar/Project/Python/DogAI/dog_inflammation
def main():
    # Check if the directory exists
    if not EXTRACTED_FOLDER.exists():
        print(f"Directory {EXTRACTED_FOLDER} does not exist. Please check the path or create the directory.")
        return

    # Check if 'train' and 'valid' subdirectories exist
    train_path = EXTRACTED_FOLDER / 'train'
    valid_path = EXTRACTED_FOLDER / 'valid'
    
    if not train_path.exists() or not valid_path.exists():
        print(f"Subdirectories 'train' or 'valid' do not exist within {EXTRACTED_FOLDER}.")
        return

    print("Directory structure is correct. Attempting to create DataLoaders...")

    # Print contents of the data folder for verification
    print(f"Contents of {EXTRACTED_FOLDER}: {list(EXTRACTED_FOLDER.glob('*'))}")
    print(f"Contents of {train_path}: {list(train_path.glob('*'))}")
    print(f"Contents of {valid_path}: {list(valid_path.glob('*'))}")

    # Define the data loaders
    try:
        dls = ImageDataLoaders.from_folder(
            EXTRACTED_FOLDER,
            train='train',
            valid='valid',
            item_tfms=Resize(128),  # Transforms applied to each image item
            batch_tfms=aug_transforms()  # Optional batch transformations
        )
        print("DataLoaders created successfully.")
    except Exception as e:
        print(f"An error occurred while creating DataLoaders: {e}")
        return

    # Initialize the model
    try:
        learn = cnn_learner(dls, resnet34, metrics=accuracy)
        print("Model initialized successfully.")
    except Exception as e:
        print(f"An error occurred while initializing the model: {e}")
        return

    # Optionally, load a pre-trained model
    try:
        learn.load('best_model')
        print("Model loaded successfully.")
    except FileNotFoundError:
        print("Pre-trained model not found. Training a new model.")
        learn.fine_tune(4)  # Train the model if pre-trained model is not available

    # Evaluate the model
    evaluate_model(learn)

def evaluate_model(learn):
    # Define paths for test images
    neg_path = EXTRACTED_FOLDER / 'test_images/Negative/D0_03f7e7c0-60a5-11ec-8402-0a7404972c70.jpg'
    pos_path = EXTRACTED_FOLDER / 'test_images/Positive/D0_02fa7d26-60a5-11ec-8402-0a7404972c70.jpg'
    
    # Check if image files exist
    if not neg_path.exists():
        raise FileNotFoundError(f"Negative image file {neg_path} does not exist.")
    if not pos_path.exists():
        raise FileNotFoundError(f"Positive image file {pos_path} does not exist.")
    
    print("Test image files found. Creating DataLoader for evaluation...")

    # Create DataLoader for evaluation
    try:
        test_dl = learn.dls.test_dl([neg_path, pos_path])
        if len(test_dl.dataset) == 0:
            raise ValueError("Test DataLoader contains no data.")
        print("DataLoader for evaluation created successfully.")
    except Exception as e:
        print(f"An error occurred while creating DataLoader for evaluation: {e}")
        return

    # Get predictions
    try:
        preds, targs = learn.get_preds(dl=test_dl)
        if preds is None or targs is None:
            raise ValueError("Predictions or targets are None.")
        print("Predictions and targets obtained successfully.")
    except Exception as e:
        print(f"An error occurred while obtaining predictions: {e}")
        return

    # Display results
    for i, (img, pred, targ) in enumerate(zip(test_dl.items, preds, targs)):
        img.show()
        plt.title(f'Predicted: {learn.dls.vocab[pred.argmax()]} | Actual: {learn.dls.vocab[targ]}')
        plt.show()
    print("Evaluation complete.")

if __name__ == "__main__":
    main()
