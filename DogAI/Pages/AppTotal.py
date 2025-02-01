from fastai.vision.all import *
import matplotlib.pyplot as plt
from pathlib import Path

EXTRACTED_FOLDER = Path('/Users/rainstar/Project/Python/Dog AI/dog_inflammation/dog-inflammation')

def main():
    # Define data loaders
    dls = ImageDataLoaders.from_folder(
        EXTRACTED_FOLDER, 
        train='train', 
        valid='valid', 
        item_tfms=Resize(128)
    )

    # Initialize the model
    learn = cnn_learner(dls, resnet34, metrics=accuracy)

    # Optionally, load a pre-trained model
    learn.load('best_model')

    # Evaluate the model
    evaluate_model(learn)

def evaluate_model(learn):
    # Define paths for test images
    neg_path = EXTRACTED_FOLDER / 'Negative/D0_03f7e7c0-60a5-11ec-8402-0a7404972c70.jpg'
    pos_path = EXTRACTED_FOLDER / 'Positive/D0_02fa7d26-60a5-11ec-8402-0a7404972c70.jpg'
    
    # Check if image files exist
    if not neg_path.exists():
        raise FileNotFoundError(f"Negative image file {neg_path} does not exist.")
    if not pos_path.exists():
        raise FileNotFoundError(f"Positive image file {pos_path} does not exist.")
    
    # Create DataLoader for evaluation
    test_dl = learn.dls.test_dl([neg_path, pos_path])
    
    # Check if test_dl is correctly populated
    if len(test_dl.dataset) == 0:
        raise ValueError("Test DataLoader contains no data.")
    
    # Get predictions
    preds, targs = learn.get_preds(dl=test_dl)
    
    # Debugging: Check if preds and targs are None
    if preds is None or targs is None:
        raise ValueError("Predictions or targets are None.")
    
    # Display results
    for i, (img, pred, targ) in enumerate(zip(test_dl.items, preds, targs)):
        img.show()
        plt.title(f'Predicted: {learn.dls.vocab[pred.argmax()]} | Actual: {learn.dls.vocab[targ]}')
        plt.show()
    print("Evaluation complete.")

if __name__ == "__main__":
    main()
