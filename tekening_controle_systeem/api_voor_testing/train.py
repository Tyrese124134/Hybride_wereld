import os
import cv2
import random
import numpy as np
import pandas as pd

from PIL import Image

import torch
import torch.nn as nn
import torch.optim as optim

from torchvision import transforms
from torchvision import models

from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from torch.utils.data import random_split



MEMORY_SAFE = "memory/safe"
MEMORY_UNSAFE = "memory/unsafe"

PICKLE_DATASET = "./dataset/proccesed_data.pkl"

MODEL_SAVE_PATH = (
    "model/resnet18_sketch_model_best.pth"
)

BATCH_SIZE = 32

EPOCHS = 10

LEARNING_RATE = 0.0001

DEVICE = (
    "cuda"
    if torch.cuda.is_available()
    else "cpu"
)



print("\nLoading original dataset...\n")

df = pd.read_pickle(
    PICKLE_DATASET
)

X = list(
    df["sketch_image"].values
)

y = list(
    df["label"].values
)

print(
    f"Original dataset loaded: {len(X)} images"
)



print("\nLoading memory dataset...\n")

def load_memory_images(folder, label):

    images = []
    labels = []

    for filename in os.listdir(folder):

        filepath = os.path.join(
            folder,
            filename
        )

        try:

            image = cv2.imread(
                filepath,
                cv2.IMREAD_GRAYSCALE
            )

            if image is None:
                continue

            images.append(image)

            labels.append(label)

        except Exception as e:

            print(
                f"Error loading {filepath}: {e}"
            )

    return images, labels

# SAFE

safe_images, safe_labels = load_memory_images(
    MEMORY_SAFE,
    0
)

# UNSAFE

unsafe_images, unsafe_labels = load_memory_images(
    MEMORY_UNSAFE,
    1
)

# ADD TO DATASET

X.extend(safe_images)
X.extend(unsafe_images)

y.extend(safe_labels)
y.extend(unsafe_labels)

print(
    f"Memory safe images: {len(safe_images)}"
)

print(
    f"Memory unsafe images: {len(unsafe_images)}"
)

print(
    f"Total dataset size: {len(X)}"
)




transform = transforms.Compose([

    transforms.ToPILImage(),

    transforms.Resize(
        (224, 224)
    ),

    transforms.Grayscale(
        num_output_channels=3
    ),

    transforms.RandomRotation(
        10
    ),

    transforms.RandomHorizontalFlip(),

    transforms.ToTensor(),

    transforms.Normalize(

        mean=[0.485, 0.456, 0.406],

        std=[0.229, 0.224, 0.225]
    )
])


class SketchDataset(Dataset):

    def __init__(
        self,
        X,
        y,
        transform=None
    ):

        self.X = X

        self.y = y

        self.transform = transform

    def __len__(self):

        return len(self.X)

    def __getitem__(self, idx):

        image = self.X[idx]

        label = self.y[idx]

        # convert float arrays

        if isinstance(image, np.ndarray):

            image = image.astype(
                np.uint8
            )

        if self.transform:

            image = self.transform(
                image
            )

        return (

            image,

            torch.tensor(
                label,
                dtype=torch.long
            )
        )



dataset = SketchDataset(

    X,
    y,
    transform=transform
)



train_size = int(
    0.8 * len(dataset)
)

val_size = (
    len(dataset) - train_size
)

train_dataset, val_dataset = random_split(

    dataset,

    [train_size, val_size]
)



train_loader = DataLoader(

    train_dataset,

    batch_size=BATCH_SIZE,

    shuffle=True
)

val_loader = DataLoader(

    val_dataset,

    batch_size=BATCH_SIZE,

    shuffle=False
)



print("\nLoading ResNet18...\n")

model = models.resnet18(
    weights="DEFAULT"
)

num_features = model.fc.in_features

model.fc = nn.Linear(

    num_features,

    2
)

model = model.to(DEVICE)


criterion = nn.CrossEntropyLoss()

optimizer = optim.Adam(

    model.parameters(),

    lr=LEARNING_RATE
)



best_accuracy = 0

print("\nStarting training...\n")

for epoch in range(EPOCHS):



    model.train()

    running_loss = 0

    train_correct = 0

    train_total = 0

    for images, labels in train_loader:

        images = images.to(DEVICE)

        labels = labels.to(DEVICE)

        optimizer.zero_grad()

        outputs = model(images)

        loss = criterion(
            outputs,
            labels
        )

        loss.backward()

        optimizer.step()

        running_loss += loss.item()

        _, predicted = torch.max(
            outputs,
            1
        )

        train_total += labels.size(0)

        train_correct += (
            predicted == labels
        ).sum().item()

    train_accuracy = (
        100 * train_correct / train_total
    )



    model.eval()

    val_correct = 0

    val_total = 0

    with torch.no_grad():

        for images, labels in val_loader:

            images = images.to(DEVICE)

            labels = labels.to(DEVICE)

            outputs = model(images)

            _, predicted = torch.max(
                outputs,
                1
            )

            val_total += labels.size(0)

            val_correct += (
                predicted == labels
            ).sum().item()

    val_accuracy = (
        100 * val_correct / val_total
    )

    print(

        f"\nEpoch [{epoch+1}/{EPOCHS}]"

        f"\nLoss: {running_loss:.4f}"

        f"\nTrain Accuracy: "
        f"{train_accuracy:.2f}%"

        f"\nValidation Accuracy: "
        f"{val_accuracy:.2f}%"
    )



    if val_accuracy > best_accuracy:

        best_accuracy = val_accuracy

        torch.save(

            model.state_dict(),

            MODEL_SAVE_PATH
        )

        print(
            "\nBest model saved.\n"
        )



print("\nTraining complete.")

print(

    f"\nBest Validation Accuracy: "
    f"{best_accuracy:.2f}%"
)

print(
    f"\nModel saved to:\n"
    f"{MODEL_SAVE_PATH}"
)