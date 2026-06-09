# Unreal Engine – Leuvehaven kamer Immersieve Ervaring

## projectoverzicht

Dit Unreal Engine project is ontwikkeld voor een interactieve historische museumervaring gebasseerd op de stijlkamer van de Leuvehaven in het Schielandshuis.

Het doel van de omgeving is om geschiedenis digitaal tot leven te brengen door middel van een combinatie van: 

- 3D–modellen
- Cinematische camera's
- Belichting
- Omgevingsgeluiden
- Visuele effecten
- Interactieve bezoekersbijdragen

De ervaring is ontworpen als een digitale uitbreiding van de fysieke expositie.

---

# Technische informatie

**Engine:** Unreal Engine 5.7
**Project:** NPC_ontwikkeling
**Hoofdlecel:** LV_Intro
**Sequence:** LS_Intro

Belangrijke onderdelen:

- Blender FBX imports
- Environment systeem
- CinecameraActor 
- Unreal Sequencer
- Audio systeem
- Niagara VFX
- Image Streaming

---

# Projectstructuur

```
Content 

│ 

├── Environment 

│   ├── Muur_Links 

│   ├── Muur_Midden 

│   └── Muur_Rechts 

│ 

├── Audio 

│   ├── Ambience 

│   ├── Fireplace 

│   └── Wind 

│ 

├── Sequencer 

│   └── LS_Intro 
│ 

└── VFX 

    └── Fire 
``` 
---

# Ontwikkelde onderdelen

## Blender omgeving

De historische muren zijn ontwikkeld in Blender en geïmporteerd in Unreal Enginevia FBX bestanden.

Ontwikkeling: 
- Rechter muur -> Pepijn
- Midden en linker muur -> Abigail 
- Ingeladen en aangepast door Tyrese

Na import zijn verschillende onderdelen aangepast:

- Materials
- Textures
- Positionering
- Schaal
- Rotatie

---

## Cinematic systeem

De ervaring gebruikt Unreal Sequencer om automarisch een cameraverhaal af te spelen.

Sequence:

`LS_Intro`

Bevat: 
- CineCameraActor
- Camera Cuts
- Camera beweging
- Audio tracks

Wanneer het level gestart wordt begint de ervaring automatisch vanuit het cameraperspectief.



Playback:
```
Auto Play: Enabled
Loop: Loop indefinitely
```
Hierdoor kan de ervaring continu draaien tijdens een expositie.

--- 

## Audio systeem

Voor extra immersie zijn meerdere geluidslagen toegevoegd:

- Kamer ambience
- Wind geluid
- Openhaard geluid

De audio wordt afgespeeld via Sequencer en loopt synchroon met de ervaring.

---

## Fire VFX

Voor de openhaard is een bewegend vuur toegevoegd met behulp van Unreal VFX.

Gebruikt:

- Niagara particle system
- Fire asset vanuit FAB marketplace

Dit zorgt voor meer sfeer en realisme binnen de kamer.

---

## Prototype onderdelen

Tijdens de ontwikkeling zijn verschillende prototypes gemaakt:

### Subtitle systeem
Een automatisch ondertitelingssysteem gebouw met:

- Widget Blueprints
- Levek Blueprints
- Timers

### AI Voice systeem
Een AI voice-over prototype gemaakt en gekoppeld met de subtitles. 

Deze onderdelen zijn later verwijderd vanwege een conecptwijzigingen waarbij de focus meer kwam te liggen op sfeer en achtergrondgeluid. 

---

## Image Streaming systeem

Voor bezoekersinteracite is een systeem ontwikkeld waarbij tekeningen digitaal toegevoegd kunnen worden aan de kamer.

Proces: 
1. Bezoeker maakt een tekening
2. Webapplicatie verwerkt de afbeelding
3. API-server verstuurt de afbeelding
4. Unreal Engine toont de afbeelding op de muur

---

# Project opnieuw opbouwen

## Stap 1 – Project openen

Gebruik: 

- Unreal Engine 5.7
- Third Person template

Open: 

```
LV_Intro
```
---

## Stap 2 – Environment toevoegen

Importeer de Blender FBX bestanden.

Controleer:

- scale
- Rotation
- Position
- Materials

---

## stap 3 – Sequencer instellen

Maak een nieuwe Level sequence.

Voeg toe:

- Camera Cut Track
- CineCameraActor

---

## Stap 4 – Belichting toevoegen

Gebruik:

- Directional Light
- Point light

pas deze aan voor de gewenste sfeer.

---

## Stap 5 – Audio toevoegen

Importeer audio bestanden naar:

```
Content/audio
```
Voeg deze toe aan:

```
LS_Intro
```

---

## Stap 6 – Extra omgeving

Toevoegen:

- vloer
- Extra objecten
- VFX effecten
- Historische elementen

---
# Mogelijke uitbreidingen 

 

- Extra camera shots 

- Verbeterde belichting 

- NPC animaties Jan & Pieter 

- Meer historische objecten 

- Uitgebreidere bezoekersinteractie 

 

--- 

 

# Belangrijke bestanden 

 

| Bestand | Beschrijving | 

|---|---| 

| LV_Intro | Hoofdlevel | 

| LS_Intro | Cinematic sequence | 

| CineCameraActor | Camera ervaring | 

| Environment | Blender modellen | 

| Audio | Omgevingsgeluiden | 

| Fire VFX | Openhaard effect | 

 

--- 

 

## Status 

 

De basis van de interactieve historische ervaring is werkend: 

 

✔ Kameromgeving   

✔ Cinematic camera   

✔ Audio systeem   

✔ Loop systeem   

✔ Fire VFX   

✔ Image streaming voorbereiding   