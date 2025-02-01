from fastai.vision.all import *

EXTRACTED_FOLDER = Path('/Users/rainstar/Project/Python/DogAI/dog_inflammation')

def main():
    # Define the data loaders
    dls = ImageDataLoaders.from_folder(
        EXTRACTED_FOLDER,
        train='train',
        valid='valid',
        item_tfms=Resize(128),  # Transforms applied to each image item
        batch_tfms=aug_transforms()  # Optional batch transformations
    )
    
    # Initialize the model
    learn = cnn_learner(dls, resnet34, metrics=accuracy)
    
    # Train the model
    learn.fine_tune(4)  # You can specify the number of epochs here

    # Save the model
    model_path = '/Users/rainstar/Project/Python/DogAI/dog_inflammation/model.pth'
    learn.export(model_path)  # Saves the model and data
    print(f"Model saved to {model_path}")

if __name__ == '__main__':
    main()
