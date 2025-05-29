# Language Identification and Translation Pipeline

## 🧠 Objectif du projet

Ce projet vise à détecter automatiquement la langue d'un fichier audio, à transcrire son contenu via **Whisper**, le **traduire** dans une langue cible, et enfin à **générer de l'audio** dans cette langue traduite à l'aide de **gTTS (Google Text-To-Speech)**.

---

## 📊 Données utilisées

### 🗣️ Entraînement
- **Durée totale** : ~2h
- **Sources** : livres audio, journaux télévisés, podcasts (YouTube, Librivox, EU Speech Repository)
- **Caractéristiques** :
  - Format : `.wav`, stéréo, 44kHz
  - Répartition : 3 min par locuteur
  - 20 femmes et 20 hommes
  - Langues : Français, Anglais, Espagnol, Arabe Classique, Darija (dialecte marocain), Coréen

### 🧪 Test
- **Durée totale** : ~20 min
- **Caractéristiques** :
  - 30 secondes par fichier audio
  - 20 femmes et 20 hommes
  - Même langues que pour l'entraînement

---

## 🔍 Étapes du pipeline

### 1. **Extraction de caractéristiques**
- Extraction des **MFCC** (13), ainsi que leurs dérivées :
  - ΔMFCC (delta)
  - Δ²MFCC (delta²)
- Total de **39 dimensions**

### 2. **Entraînement des modèles GMM**
- Pour chaque langue, entraînement de modèles GMM avec :
  - **8, 16, 32, 64, 128, 256, 512, 1024 gaussiennes**
- Stockage dans `gmm_models_pkl/`

### 3. **Évaluation**
- Mesure de l’accuracy et génération des **matrices de confusion**
- Résultats :
  - Sans normalisation (39D) :
    - **Accuracy max : 81%** sur 4 langues
  - Avec **normalisation des MFCC** :
    - **Accuracy : 95%** sur 4 langues
    - **Accuracy : 81%** sur 6 langues

---
