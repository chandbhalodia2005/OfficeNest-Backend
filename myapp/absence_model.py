# your_project/your_app/absence_model.py

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
from datetime import timedelta, datetime
import os
import numpy as np

class AbsentPredictor:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
        self.features = ['user_email_encoded', 'user_role_encoded', 'day_of_week', 'month', 'previous_absences_7d']
        self.encoder_data = {} # To store factorization data for consistent encoding

    def preprocess_data(self, attendance_records):
        df = pd.DataFrame(list(attendance_records))

        if df.empty:
            return None

        df['is_absent'] = df['real_entry_time'].isnull().astype(int)
        df['date'] = pd.to_datetime(df['date'])
        df['day_of_week'] = df['date'].dt.weekday
        df['month'] = df['date'].dt.month

        df = df.sort_values(by=["user_email", "date"])
        df['previous_absences_7d'] = df.groupby('user_email')['is_absent'].rolling(7, min_periods=1).sum().reset_index(level=0, drop=True) - df['is_absent']

        df['user_email_encoded'], self.encoder_data['user_email_classes'] = pd.factorize(df['user_email'])
        df['user_role_encoded'], self.encoder_data['user_role_classes'] = pd.factorize(df['user_role'])
        
        return df

    def train_model(self, df):
        if len(df['is_absent'].unique()) < 2:
            return False

        X = df[self.features]
        y = df['is_absent']
        
        self.model.fit(X, y)
        return True

    def predict_absence_probabilities(self, df):
        if df is None or df.empty:
            return []

        user_predictions = {}
        unique_users = df[['user_email', 'user_name', 'user_role', 'user_email_encoded', 'user_role_encoded', 'previous_absences_7d']].drop_duplicates(subset=['user_email'])
        
        today = datetime.now().date()
        for _, user in unique_users.iterrows():
            future_dates = pd.to_datetime([today + timedelta(days=d) for d in range(30)])
            
            # Create a static feature dataframe for future prediction
            future_df = pd.DataFrame({
                'user_email_encoded': [user['user_email_encoded']] * len(future_dates),
                'user_role_encoded': [user['user_role_encoded']] * len(future_dates),
                'day_of_week': future_dates.dayofweek,
                'month': future_dates.month,
                'previous_absences_7d': [user['previous_absences_7d']] * len(future_dates)
            })

            future_df = future_df[future_df['day_of_week'] < 5] # Exclude weekends

            if not future_df.empty:
                predictions = self.model.predict_proba(future_df[self.features])[:, 1]
                avg_absence_probability = predictions.mean() * 100
            else:
                avg_absence_probability = 0
            
            user_predictions[user['user_email']] = {
                "name": user['user_name'],
                "role": user['user_role'].capitalize(),
                "absenceScore": round(avg_absence_probability, 2)
            }
        
        predictions = sorted(user_predictions.values(), key=lambda x: x['absenceScore'], reverse=True)
        return predictions