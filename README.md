# Enterprise AI Customer Churn Predictor

An end-to-end, full-stack machine learning application that predicts the likelihood of a customer canceling their service (churning). It utilizes a Scikit-Learn machine learning pipeline, a Flask REST API, a PostgreSQL database for historical logging, and a stunning glassmorphism interactive frontend.

## 🌟 Features
- **Predictive ML Pipeline:** Uses a pre-trained scikit-learn model (`churn_model.pkl`) to analyze 19 different customer data points.
- **Interactive UI:** A highly polished, dark-mode frontend featuring dynamic animations, glowing orbs, and real-time prediction feedback.
- **RESTful API:** Exposes a `/predict` endpoint that accepts JSON payloads for programmatic access.
- **Database Logging:** Automatically records all user inputs and model predictions into a local SQLite database (or PostgreSQL in production) using SQLAlchemy.
- **Cloud-Ready:** Fully configured for instant deployment on Railway or AWS using Gunicorn.

## 🛠️ Tech Stack
- **Backend:** Python, Flask, Gunicorn
- **Machine Learning:** Scikit-Learn, Pandas, Joblib
- **Database:** SQLAlchemy (SQLite locally, PostgreSQL in production)
- **Frontend:** Vanilla HTML5, CSS3 (Glassmorphism design), JavaScript
- **Fonts & Icons:** Google Fonts (Inter, Outfit), FontAwesome

## 🚀 How to Run Locally

1. **Ensure Python is installed** (Python 3.9+ recommended).
2. **Install the dependencies:**
   Open your terminal in the project folder and run:
   ```bash
   pip install -r requirements.txt
   ```
3. **Start the application:**
   ```bash
   python application.py
   ```
4. **Access the Dashboard:**
   Open your web browser and go to: `http://127.0.0.1:5000`

*Note: When run locally, the app will automatically create a `predictions.db` SQLite file to store your history. No database setup is required for local testing!*

## ☁️ Deployment (Railway)
This project is configured for 1-click deployment on Railway.app.
1. Push this repository to GitHub.
2. Connect your GitHub to Railway and deploy the repository.
3. Add a PostgreSQL Database service in Railway.
4. Link the `DATABASE_URL` variable to your web service.
5. Railway will automatically use the included `Procfile` and `requirements.txt` to serve the app globally!

## 📡 API Usage
You can bypass the frontend and interact directly with the API by sending a `POST` request to the `/predict` endpoint.

**Endpoint:** `POST /predict`
**Content-Type:** `application/json`

**Example Payload:**
```json
{
    "input": {
        "gender": "Female",
        "seniorcitizen": 1,
        "partner": "No",
        "dependents": "No",
        "tenure": 1,
        "phoneservice": "Yes",
        "multiplelines": "Yes",
        "internetservice": "Fiber optic",
        "onlinesecurity": "No",
        "onlinebackup": "No",
        "deviceprotection": "No",
        "techsupport": "No",
        "streamingtv": "Yes",
        "streamingmovies": "Yes",
        "contract": "Month-to-month",
        "paperlessbilling": "Yes",
        "paymentmethod": "Electronic check",
        "monthlycharges": 95.0,
        "totalcharges": 95.0
    }
}
```

**Expected Response:**
```json
{
    "prediction": 1
}
```
*(0 = Retained, 1 = High Churn Risk)*
