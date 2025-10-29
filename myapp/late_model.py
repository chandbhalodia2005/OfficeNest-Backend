# your_project/your_app/late_model.py

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from datetime import timedelta, datetime
import os
import joblib

class LatePredictor:
    def __init__(self):
        # Initialize the model and features
        self.model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
        self.features = ['user_id_encoded', 'user_role_encoded', 'day_of_week', 'month']
        self.encoders = {}

    def preprocess_data(self, attendance_records, today):
        """Preprocesses raw attendance data into a DataFrame with features."""
        df = pd.DataFrame(list(attendance_records))

        if df.empty:
            return None

        df['date'] = pd.to_datetime(df['date'])

        # Create the target variable 'is_late'
        df['is_late'] = df.apply(
            lambda row: 1 if datetime.combine(today, row['real_entry_time']) > datetime.combine(today, row['expected_entry_time']) + timedelta(minutes=30) else 0,
            axis=1
        )
        
        # Create features
        df['day_of_week'] = df['date'].dt.dayofweek
        df['month'] = df['date'].dt.month
        
        # Robust categorical encoding
        df['user_id_encoded'], self.encoders['user_id_labels'] = pd.factorize(df['user_email'])
        df['user_role_encoded'], self.encoders['user_role_labels'] = pd.factorize(df['user_role'])

        return df

    def train_model(self, df):
        """Trains the Random Forest Classifier model."""
        if df is None or len(df['is_late'].unique()) < 2:
            return False

        X = df[self.features]
        y = df['is_late']
        self.model.fit(X, y)
        return True

    def predict_future_lateness(self, df, today):
        """Predicts late probabilities for the next month for all users."""
        if df is None:
            return []

        user_predictions = {}
        unique_users = df[['user_email', 'user_id_encoded', 'user_name', 'user_role', 'user_role_encoded']].drop_duplicates()
        
        if unique_users.empty:
            return []

        for _, user in unique_users.iterrows():
            future_dates = pd.to_datetime([today + timedelta(days=d) for d in range(30)])
            future_df = pd.DataFrame({
                'user_id_encoded': [user['user_id_encoded']] * len(future_dates),
                'user_role_encoded': [user['user_role_encoded']] * len(future_dates),
                'day_of_week': future_dates.dayofweek,
                'month': future_dates.month
            })
            
            # Filter for weekdays
            future_df = future_df[future_df['day_of_week'] < 5]

            if not future_df.empty:
                # Get the probability of being late (class 1)
                predictions = self.model.predict_proba(future_df[self.features])[:, 1]
                avg_late_probability = predictions.mean() * 100
            else:
                avg_late_probability = 0
            
            user_predictions[user['user_email']] = {
                'name': user['user_name'],
                'role': user['user_role'],
                'late_score': round(avg_late_probability, 2)
            }
        
        sorted_late_users = sorted(user_predictions.values(), key=lambda x: x['late_score'], reverse=True)
        return sorted_late_users