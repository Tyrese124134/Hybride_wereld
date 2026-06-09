# AI Drawing Moderation System
Een AI-gestuurd moderatiesysteem dat tekeningen analyseert en automatisch classificeert als Safe of Unsafe.

Het systeem combineert Computer Vision, Deep Learning en een feedbackmechanisme waarmee het model verbeterd kan worden door nieuwe voorbeelden.

Het project is ontwikkeld als onderzoek naar automatische contentmoderatie binnen een interactieve digitale omgeving.


⸻


## Projectdoel
Het doel van dit project is het ontwikkelen van een intelligent systeem dat gebruikerscontent automatisch kan controleren voordat deze wordt weergegeven.

Het systeem kan:

Afbeeldingen analyseren

Ongewenste visuele content herkennen

Safe / Unsafe voorspellingen maken

Gebruikersfeedback verzamelen

Nieuwe voorbeelden opslaan

Verbeterd worden door retraining

Hierdoor ontstaat een AI-systeem dat niet alleen voorspellingen maakt, maar ook verder verbeterd kan worden.


⸻


## Machine Learning Aanpak
Fase 1: Eigen CNN Model
Als eerste experiment is een eigen Convolutional Neural Network (CNN) ontwikkeld.

Doel:

Begrijpen hoe beeldclassificatie werkt

Een eerste baseline creëren

Resultaat:

Accuracy: ±59%

Het model had moeite met complexe patronen en verschillen tussen klassen

Daarom is gekozen voor transfer learning.


⸻

Fase 2: ResNet18 Transfer Learning
Voor de verbeterde versie is gebruikgemaakt van een vooraf getraind ResNet18-model.

Waarom ResNet18?

Voorgetraind op grote hoeveelheden afbeeldingen

Herkent algemene vormen en patronen

Minder trainingsdata nodig

Betere prestaties dan een eigen CNN

Eerste resultaten:

Accuracy: ±68%

Na uitbreiding met feedbackdata:

Validation Accuracy: ±75%


⸻


## Dataset
Voor training is gebruikgemaakt van de UnsafeBench Dataset.

De dataset bevat:

Safe afbeeldingen

Unsafe afbeeldingen

Classificatie labels

Tijdens preprocessing:

Afbeeldingen opgeschoond

Dubbele data verwijderd

Afbeeldingen geschaald

Sketch-versies gegenereerd

Labels voorbereid voor training

Omdat het uiteindelijke systeem tekeningen moet beoordelen, zijn afbeeldingen omgezet naar een meer schetsachtige stijl.


⸻


## Feedback Learning Systeem
Het systeem bevat een geheugenmechanisme waarmee gebruikers voorspellingen kunnen verbeteren.

Structuur:

memory/

├── safe/

└── unsafe/

Wanneer een voorspelling fout is:

Gebruiker geeft feedback

Afbeelding wordt opgeslagen

Correct label wordt bewaard

Nieuwe data wordt gebruikt tijdens retraining

Hierdoor kan het model steeds verder verbeterd worden.


⸻


## Projectstructuur
project/

│

├── notebooks/

│   ├── drawing.ipynb

│   └── data_eda.ipynb

│

├── api_voor_testing/

│   ├── app.py

│   ├── train.py

│   └── memory/

│

├── app/

│   └── app2.py

│

├── model/

│   └── resnet18_sketch_model.pth

│

├── requirements.txt

├── Dockerfile

└── README.md


⸻


## Belangrijke Bestanden
drawing.ipynb
Bevat het volledige machine learning proces:

Dataset laden

Preprocessing

Sketch generatie

Eigen CNN experiment

ResNet18 training

Model evaluatie


⸻

## data_eda.ipynb
Exploratory Data Analysis:

Dataset onderzoeken

Klasseverdeling bekijken

Datakwaliteit controleren


⸻

## api_voor_testing/app.py
Volledige FastAPI testomgeving.

Functionaliteiten:

Webinterface

Afbeeldingen uploaden

AI voorspellingen

Feedback geven

Logging

Moderatiegeschiedenis bekijken


⸻

## api_voor_testing/train.py
Script voor modelverbetering.

Ondersteunt:

Dataset laden

Feedbackdata toevoegen

Data augmentation

Transfer learning

Validatie

Automatisch beste model opslaan


⸻

## app/app2.py
Lichtgewicht API-versie voor integratie.

Bevat:

✔ Upload endpoint

✔ Model voorspelling

✔ JSON response

Niet aanwezig:

❌ Webinterface

❌ Feedback dashboard

❌ Logging pagina

Deze versie is geschikt voor deployment.


⸻


API Endpoints
Upload & Predict
POST:

/predict

Input:

image file

Output:

{

 "prediction": "Safe",

 "confidence": 0.92

}


⸻

Feedback
POST:

/feedback

Slaat correcties van gebruikers op.


⸻

Logs
GET:

/logs

Geeft eerdere voorspellingen terug.


⸻

Health Check
GET:

/health

Output:

{

 "status": "running"

}


⸻

## Installatie
Clone repository:

git clone <repository-url>

cd project

Maak virtual environment:

python -m venv venv

Windows:

venv\Scripts\activate

Linux / macOS:

source venv/bin/activate

Installeer packages:

pip install -r requirements.txt


⸻


## Applicatie Starten
FastAPI starten:

uvicorn app:app --reload

Open:

http://localhost:8000


⸻


Docker
Build:

docker build -t drawing-moderation .

Run:

docker run -p 8000:8000 drawing-moderation


⸻


Technologieën
Python

PyTorch

Torchvision

ResNet18

FastAPI

Docker

OpenCV

NumPy

Pandas

Scikit-Learn

Jinja2


⸻


## Responsible AI
Omdat het systeem automatisch gebruikerscontent beoordeelt, zijn AI-risico’s meegenomen.

Belangrijke punten:

AI kan fouten maken

Gebruikersfeedback blijft mogelijk

Data wordt verder verbeterd

Menselijke controle blijft belangrijk

Bias in trainingsdata moet gecontroleerd worden

Het systeem ondersteunt daarom een human-in-the-loop aanpak.


⸻


Toekomstige Verbeteringen
Mogelijke uitbreidingen:

Grotere trainingsdataset

Verbeterde unsafe detectie

OCR voor tekst in tekeningen

Multi-label classificatie

Automatische retraining pipeline

Cloud deployment

Real-time moderatie


⸻


## Auteur
Ontwikkeld als onderdeel van een onderzoek naar AI-gestuurde contentmoderatie.

Het project laat zien hoe Computer Vision, Transfer Learning, FastAPI en feedbackgestuurde verbetering gecombineerd kunnen worden tot een praktisch AI-moderatiesystee
 