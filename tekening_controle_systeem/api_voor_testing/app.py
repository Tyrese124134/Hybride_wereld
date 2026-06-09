from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from PIL import Image

import io
import os
import json
import hashlib
import shutil

from datetime import datetime

import torch
import torchvision.transforms as transforms
import torch.nn as nn
import torchvision.models as models



app = FastAPI()



UPLOAD_FOLDER = "uploads"
STATIC_FOLDER = "static"

SAFE_MEMORY = "memory/safe"
UNSAFE_MEMORY = "memory/unsafe"

MODEL_PATH = "model/resnet18_sketch_model_best.pth"

LOG_FILE = "moderation_log.json"


# ============================================
# CREATE DIRECTORIES
# ============================================

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

os.makedirs(
    STATIC_FOLDER,
    exist_ok=True
)

os.makedirs(
    SAFE_MEMORY,
    exist_ok=True
)

os.makedirs(
    UNSAFE_MEMORY,
    exist_ok=True
)



app.mount(
    "/uploads",
    StaticFiles(directory=UPLOAD_FOLDER),
    name="uploads"
)

app.mount(
    "/static",
    StaticFiles(directory=STATIC_FOLDER),
    name="static"
)



templates = Jinja2Templates(
    directory="templates"
)



if not os.path.exists(LOG_FILE):

    with open(LOG_FILE, "w") as f:

        json.dump([], f)



BLOCKED_WORDS = [

    "sex",
    "nazi",
    "rape",
    "terrorist",
    "kill",
    "suicide",
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

if os.path.exists(MODEL_PATH):

    model.load_state_dict(

        torch.load(
            MODEL_PATH,
            map_location=torch.device("cpu")
        )
    )

    print("\nModel loaded successfully.\n")

else:

    print("\nWARNING: MODEL NOT FOUND.\n")


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



@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    logs = []

    if os.path.exists(LOG_FILE):

        with open(LOG_FILE, "r") as f:

            logs = json.load(f)

    return templates.TemplateResponse(

        "index.html",

        {

            "request": request,

            "logs": logs[::-1]
        }
    )



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

                blocked_filename = (

                    f"blocked_"
                    f"{datetime.now().timestamp()}_"
                    f"{file.filename}"
                )

                blocked_path = os.path.join(
                    UNSAFE_MEMORY,
                    blocked_filename
                )

                with open(blocked_path, "wb") as f:

                    f.write(image_bytes)

                return JSONResponse({

                    "prediction": "unsafe",

                    "confidence": 1.0,

                    "reason": f"blocked_word:{word}"
                })

        filename = (

            f"{datetime.now().timestamp()}_"
            f"{file.filename}"
        )

        filepath = os.path.join(
            UPLOAD_FOLDER,
            filename
        )

        with open(filepath, "wb") as f:

            f.write(image_bytes)

        # ====================================
        # IMAGE PREPROCESSING
        # ====================================

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

        log_entry = {

            "filename": filename,

            "prediction": prediction,

            "confidence": confidence_score,

            "time": str(datetime.now()),

            "image_url": f"/uploads/{filename}",

            "reviewed": False,

            "corrected_label": None
        }

        logs = []

        with open(LOG_FILE, "r") as f:

            logs = json.load(f)

        logs.append(log_entry)

        with open(LOG_FILE, "w") as f:

            json.dump(
                logs,
                f,
                indent=4
            )

        # ====================================
        # RESPONSE
        # ====================================

        return JSONResponse({

            "prediction": prediction,

            "confidence": confidence_score,

            "filename": filename,

            "image_url": f"/uploads/{filename}"
        })

    except Exception as e:

        return JSONResponse({

            "error": str(e)
        })



@app.post("/feedback/{filename}/{label}")
async def feedback(
    filename: str,
    label: str
):

    try:

        filepath = os.path.join(
            UPLOAD_FOLDER,
            filename
        )

        if not os.path.exists(filepath):

            return {

                "error":
                "File not found"
            }


        if label == "unsafe":

            destination = os.path.join(
                UNSAFE_MEMORY,
                filename
            )

        else:

            destination = os.path.join(
                SAFE_MEMORY,
                filename
            )

        if not os.path.exists(destination):

            shutil.copy(
                filepath,
                destination
            )


        with open(LOG_FILE, "r") as f:

            logs = json.load(f)

        for log in logs:

            if log["filename"] == filename:

                log["reviewed"] = True

                log["corrected_label"] = label

        with open(LOG_FILE, "w") as f:

            json.dump(
                logs,
                f,
                indent=4
            )

        return {

            "message":
            "Feedback saved"
        }

    except Exception as e:

        return {

            "error":
            str(e)
        }



@app.delete("/delete-log/{filename}")
async def delete_log(filename: str):

    try:


        with open(LOG_FILE, "r") as f:

            logs = json.load(f)

        updated_logs = [

            log for log in logs

            if log["filename"] != filename
        ]


        with open(LOG_FILE, "w") as f:

            json.dump(
                updated_logs,
                f,
                indent=4
            )


        filepath = os.path.join(
            UPLOAD_FOLDER,
            filename
        )

        if os.path.exists(filepath):

            os.remove(filepath)

        return {

            "message":
            "Log deleted"
        }

    except Exception as e:

        return {

            "error":
            str(e)
        }



@app.get("/logs")
async def get_logs():

    with open(LOG_FILE, "r") as f:

        logs = json.load(f)

    return logs[::-1]



@app.get("/health")
async def health():

    return {

        "status": "running"
    }