# model_training.py

from fastai.vision.all import *
from pathlib import Path

# Define the path to your dataset
path = Path('/Users/rainstar/Project/Python/DogAI/dog_inflammation/dog-inflammation')

# Ensure the dataset directory exists
if not path.exists():
    raise FileNotFoundError(f"Dataset directory {path} does not exist.")

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

# Define and train the model
learn = vision_learner(dls, resnet18, metrics=accuracy)
learn.fine_tune(3)

# Ensure the directory for saving the model exists
model_dir = Path('models')
model_dir.mkdir(parents=True, exist_ok=True)  # Create the directory if it does not exist

# Save the model
try:
    learn.export(model_dir / 'best_model.pkl')  # Save with .pkl extension
    print("Model exported successfully.")
except Exception as e:
    raise RuntimeError(f"Failed to export the model: {e}")
