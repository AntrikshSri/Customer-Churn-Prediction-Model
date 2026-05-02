from flask import Flask, request, jsonify, render_template
import joblib
application = Flask(__name__)
model=joblib.load("churn_model.pkl")
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

        return jsonify({'prediction': int(prediction[0])})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
if __name__ == '__main__':
    application.run()