from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse

from PIL import Image

import io
import os
import hashlib

import torch
import torch.nn as nn
import torchvision.transforms as transforms
import torchvision.models as models



app = FastAPI()



MODEL_PATH = "model/resnet18_sketch_model.pth"

BLOCKED_WORDS = [

    "sex",
    "porn",
    "nigger",
    "niga",
    "nazi",
    "rape",
    "terrorist",
    "kill",
    "suicide",
    "fuck",
    "bitch",
    "slur",
    "nsfw"
]

KNOWN_UNSAFE_HASHES = set()



def get_image_hash(image_bytes):

    return hashlib.md5(
        image_bytes
    ).hexdigest()



model = models.resnet18(
    weights=None
)

model.fc = nn.Linear(
    model.fc.in_features,
    2
)

model.load_state_dict(

    torch.load(
        MODEL_PATH,
        map_location=torch.device("cpu")
    )
)

model.eval()


transform = transforms.Compose([

    transforms.Grayscale(
        num_output_channels=3
    ),

    transforms.Resize(
        (224, 224)
    ),

    transforms.ToTensor(),

    transforms.Normalize(

        mean=[0.485, 0.456, 0.406],

        std=[0.229, 0.224, 0.225]
    )
])



labels = [

    "safe",
    "unsafe"
]



@app.get("/health")
async def health():

    return {

        "status": "running"
    }



@app.post("/predict")
async def predict_image(
    file: UploadFile = File(...)
):

    try:

  
        image_bytes = await file.read()

        image_hash = get_image_hash(
            image_bytes
        )

        lower_name = file.filename.lower()


        if image_hash in KNOWN_UNSAFE_HASHES:

            return JSONResponse({

                "prediction": "unsafe",

                "confidence": 1.0,

                "reason": "known_unsafe_image"
            })


        for word in BLOCKED_WORDS:

            if word in lower_name:

                KNOWN_UNSAFE_HASHES.add(
                    image_hash
                )

                return JSONResponse({

                    "prediction": "unsafe",

                    "confidence": 1.0,

                    "reason": f"blocked_word:{word}"
                })


        image = Image.open(
            io.BytesIO(image_bytes)
        ).convert("RGB")


        image_tensor = transform(image)

        image_tensor = image_tensor.unsqueeze(0)


        with torch.no_grad():

            outputs = model(image_tensor)

            probabilities = torch.softmax(
                outputs,
                dim=1
            )

            confidence, predicted = torch.max(
                probabilities,
                1
            )

        prediction = labels[
            predicted.item()
        ]

        confidence_score = round(
            confidence.item(),
            4
        )


        if confidence_score < 0.75:

            prediction = "review_required"


        if prediction == "unsafe":

            KNOWN_UNSAFE_HASHES.add(
                image_hash
            )


        return JSONResponse({

            "prediction": prediction,

            "confidence": confidence_score
        })

    except Exception as e:

        return JSONResponse({

            "error": str(e)
        })