import os
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import joblib
from datetime import datetime

application = Flask(__name__)

# ✅ Configure Database (Railway provides DATABASE_URL, local uses SQLite)
database_url = os.environ.get('DATABASE_URL', 'sqlite:///predictions.db')
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

application.config['SQLALCHEMY_DATABASE_URI'] = database_url
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(application)

model = joblib.load("churn_model.pkl")

# ✅ Define Database Model for storing predictions
class PredictionRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Input Features
    gender = db.Column(db.String(50))
    seniorcitizen = db.Column(db.Integer)
    partner = db.Column(db.String(50))
    dependents = db.Column(db.String(50))
    tenure = db.Column(db.Integer)
    phoneservice = db.Column(db.String(50))
    multiplelines = db.Column(db.String(50))
    internetservice = db.Column(db.String(50))
    onlinesecurity = db.Column(db.String(50))
    onlinebackup = db.Column(db.String(50))
    deviceprotection = db.Column(db.String(50))
    techsupport = db.Column(db.String(50))
    streamingtv = db.Column(db.String(50))
    streamingmovies = db.Column(db.String(50))
    contract = db.Column(db.String(50))
    paperlessbilling = db.Column(db.String(50))
    paymentmethod = db.Column(db.String(50))
    monthlycharges = db.Column(db.Float)
    totalcharges = db.Column(db.Float)
    
    # Output
    prediction_result = db.Column(db.Integer)

# Create tables if they don't exist
with application.app_context():
    db.create_all()
@application.route('/')
def home():
    return render_template('index.html')
@application.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        value = data['input']

        import pandas as pd
        df = pd.DataFrame([value])

        # ✅ FIX COLUMN NAMES (match training exactly)
        df.columns = df.columns.str.strip()

        # Rename to match training
        df.rename(columns={
            "gender": "gender",

            "seniorcitizen": "SeniorCitizen",
            "partner": "Partner",
            "dependents": "Dependents",
            "tenure": "tenure",
            "phoneservice": "PhoneService",
            "multiplelines": "MultipleLines",
            "internetservice": "InternetService",
            "onlinesecurity": "OnlineSecurity",
            "onlinebackup": "OnlineBackup",
            "deviceprotection": "DeviceProtection",
            "techsupport": "TechSupport",
            "streamingtv": "StreamingTV",
            "streamingmovies": "StreamingMovies",
            "contract": "Contract",
            "paperlessbilling": "PaperlessBilling",
            "paymentmethod": "PaymentMethod",
            "monthlycharges": "MonthlyCharges",
            "totalcharges": "TotalCharges"
        }, inplace=True)

        

        # ✅ Correct Label Encoding Mapping (Matches training exactly)
        label_mappings = {
            'gender': {'Female': 0, 'Male': 1},
            'Partner': {'No': 0, 'Yes': 1},
            'Dependents': {'No': 0, 'Yes': 1},
            'PhoneService': {'No': 0, 'Yes': 1},
            'MultipleLines': {'No': 0, 'No phone service': 1, 'Yes': 2},
            'InternetService': {'DSL': 0, 'Fiber optic': 1, 'No': 2},
            'OnlineSecurity': {'No': 0, 'No internet service': 1, 'Yes': 2},
            'OnlineBackup': {'No': 0, 'No internet service': 1, 'Yes': 2},
            'DeviceProtection': {'No': 0, 'No internet service': 1, 'Yes': 2},
            'TechSupport': {'No': 0, 'No internet service': 1, 'Yes': 2},
            'StreamingTV': {'No': 0, 'No internet service': 1, 'Yes': 2},
            'StreamingMovies': {'No': 0, 'No internet service': 1, 'Yes': 2},
            'Contract': {'Month-to-month': 0, 'One year': 1, 'Two year': 2},
            'PaperlessBilling': {'No': 0, 'Yes': 1},
            'PaymentMethod': {'Bank transfer (automatic)': 0, 'Credit card (automatic)': 1, 'Electronic check': 2, 'Mailed check': 3}
        }

        for col, mapping in label_mappings.items():
            if col in df.columns:
                df[col] = df[col].map(mapping)

        # ✅ Convert numeric
        df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
        df["MonthlyCharges"] = df["MonthlyCharges"].astype(float)
        df["tenure"] = df["tenure"].astype(int)

        df = df.fillna(0)

        prediction = model.predict(df)
        pred_value = int(prediction[0])

        # ✅ Save input and output to Database
        try:
            record = PredictionRecord(
                gender=value.get('gender'),
                seniorcitizen=value.get('seniorcitizen'),
                partner=value.get('partner'),
                dependents=value.get('dependents'),
                tenure=value.get('tenure'),
                phoneservice=value.get('phoneservice'),
                multiplelines=value.get('multiplelines'),
                internetservice=value.get('internetservice'),
                onlinesecurity=value.get('onlinesecurity'),
                onlinebackup=value.get('onlinebackup'),
                deviceprotection=value.get('deviceprotection'),
                techsupport=value.get('techsupport'),
                streamingtv=value.get('streamingtv'),
                streamingmovies=value.get('streamingmovies'),
                contract=value.get('contract'),
                paperlessbilling=value.get('paperlessbilling'),
                paymentmethod=value.get('paymentmethod'),
                monthlycharges=value.get('monthlycharges'),
                totalcharges=value.get('totalcharges'),
                prediction_result=pred_value
            )
            db.session.add(record)
            db.session.commit()
        except Exception as db_err:
            print(f"Database Error: {db_err}")
            db.session.rollback()

        return jsonify({'prediction': pred_value})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
if __name__ == '__main__':
    application.run()
