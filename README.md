# 🏨 Hotel Reservation Cancellation Prediction - MLOps Project

This MLOps project predicts whether a hotel reservation will be **canceled** based on customer and booking features. It includes a full ML pipeline from data ingestion to deployment using CI/CD practices and Docker, and a user-friendly web interface built with Flask.

🌐 **Live Demo**: [Click here to try it!](https://mlops-p1-982544224719.us-central1.run.app/)

---

## 📌 Features

- 📊 Predicts if a reservation will be canceled
- ⚙️ End-to-end MLOps pipeline
- 🐳 Dockerized for containerized deployment
- 🧪 ML pipeline includes ingestion, preprocessing, training
- 📦 Integrated with Jenkins for CI/CD
- 🎯 Deployed on Google Cloud Run
- 🧠 Uses LightGBM and MLFlow for tracking

---

## 🧾 Tech Stack

| Layer           | Tools Used                                 |
|----------------|---------------------------------------------|
| ML & Modeling   | Scikit-learn, LightGBM, imbalanced-learn    |
| Tracking        | MLFlow                                      |
| Web App         | Flask + HTML/CSS                            |
| CI/CD           | Jenkins, GitHub                             |
| Containerization| Docker                                      |
| Cloud           | Google Cloud Run                            |

---

## 🚀 Web App Overview

The frontend allows users to enter details like:

- Lead time
- Special requests
- Room price
- Arrival month/date
- Meal plan, room type, etc.

🔮 After clicking **"Predict"**, the app displays whether the reservation is **likely to be canceled or not**.

![UI Screenshot](https://mlops-p1-982544224719.us-central1.run.app/static/screenshot.png) *(replace with hosted image if needed)*

---

## 🧠 Machine Learning Pipeline

### 📂 Code Modules

```bash
.
├── src/
│   ├── data_ingestion.py       # Downloads/splits data
│   ├── data_preprocessing.py   # Cleans and prepares features
│   ├── model_training.py       # Trains and saves model
│   └── custom_exception.py     # Custom error handling
├── pipeline/
│   └── training_pipeline.py    # Runs end-to-end pipeline
├── notebook/
│   └── notebook.ipynb          # EDA and experiments
```
## 🔄 Pipeline Steps

### 1.Data Ingestion:

- Loads training/test data (e.g., from GCS or local)

### 2.Preprocessing:

- Encodes categorical features

- Scales numerical data

- Handles missing values and imbalance

### 3.Model Training:

- Trains a LightGBM model

- Evaluates on test data

- Logs metrics to MLFlow

- Saves the model using joblib

## 💻 Web Application – application.py

### The Flask app:

- Loads the trained model

- Takes user input from a form

- Preprocesses and feeds it to the model

- Returns prediction result in the UI

### Prediction values:
- ✅ "The Customer is not going to cancel Reservation in future."
- ❌ "The Customer is likely to cancel Reservation."
