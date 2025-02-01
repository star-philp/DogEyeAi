# evaluate_model.py

from fastai.vision.all import *
import matplotlib.pyplot as plt
from PIL import Image

# Define the path to your saved model
model_path = Path('models/best_model.pkl')

# Ensure the model file exists
if not model_path.exists():
    raise FileNotFoundError(f"Model file {model_path} does not exist.")

# Define the path to your dataset
path = Path('/Users/rainstar/Project/Python/DogAI/dog_inflammation/dog-inflammation')

# Create a DataBlock
block = DataBlock(
    blocks=(ImageBlock, CategoryBlock),
    get_items=get_image_files,
    get_y=parent_label,
    splitter=RandomSplitter(0.2),
    item_tfms=Resize(224)
)

# Create DataLoaders
try:
    dls = block.dataloaders(path)
except Exception as e:
    raise RuntimeError(f"Failed to create DataLoaders: {e}")

# Load the trained model
try:
    learn = load_learner(model_path)
except Exception as e:
    raise RuntimeError(f"Failed to load model: {e}")

# Evaluate the model
def evaluate_model(learn):
    try:
        # Get predictions
        preds, targs = learn.get_preds(dl=dls.valid)
        
        if preds is None or targs is None:
            raise ValueError("Predictions or targets are None.")
        
        # Compute accuracy
        accuracy = (preds.argmax(dim=1) == targs).float().mean()
        print(f'Accuracy: {accuracy.item():.4f}')

        # Show a few predictions
        for img_path, pred, targ in zip(dls.valid_ds.items[:5], preds[:5], targs[:5]):
            img = Image.open(img_path)  # Load the image from path
            plt.imshow(img)
            plt.title(f'Predicted: {learn.dls.vocab[pred.argmax()]} | Actual: {learn.dls.vocab[targ]}')
            plt.axis('off')
            plt.show()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    evaluate_model(learn)
