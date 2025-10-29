# your_project/your_app/overtime_model.py

import pandas as pd
from datetime import timedelta, datetime
from sklearn.ensemble import RandomForestRegressor
import numpy as np

class OvertimePredictor:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.features = ['user_email_encoded', 'user_role_encoded', 'day_of_week', 'month', 'previous_overtime_30d']
    
    def preprocess_data(self, attendance_records):
        """Prepares the data for the model."""
        df = pd.DataFrame(list(attendance_records))

        if df.empty:
            return None

        df['date'] = pd.to_datetime(df['date'])
        df['overtime_minutes'] = df.apply(
            lambda row: max(0, (datetime.combine(row['date'], row['real_exit_time']) - datetime.combine(row['date'], row['expected_exit_time'])).total_seconds() / 60),
            axis=1
        )
        
        df['day_of_week'] = df['date'].dt.weekday
        df['month'] = df['date'].dt.month

        df = df.sort_values(by=["user_email", "date"])
        df['previous_overtime_30d'] = df.groupby('user_email')['overtime_minutes'].rolling(30, min_periods=1).sum().reset_index(level=0, drop=True) - df['overtime_minutes']
        
        df['user_email_encoded'], _ = pd.factorize(df['user_email'])
        df['user_role_encoded'], _ = pd.factorize(df['user_role'])

        return df

    def train_and_predict(self, df):
        """Trains the model and predicts future overtime."""
        if df is None or df['overtime_minutes'].sum() == 0:
            return 0

        X = df[self.features]
        y = df['overtime_minutes']
        
        self.model.fit(X, y)

        user_predictions = {}
        unique_users = df[['user_email', 'user_name', 'user_role', 'user_email_encoded', 'user_role_encoded']].drop_duplicates(subset=['user_email'])
        
        today = datetime.now().date()
        for _, user in unique_users.iterrows():
            last_record = df[df['user_email'] == user['user_email']].tail(1)
            previous_overtime_30d = last_record['previous_overtime_30d'].iloc[0] if not last_record.empty else 0

            future_dates = pd.to_datetime([today + timedelta(days=d) for d in range(30)])
            future_df = pd.DataFrame({
                'user_email_encoded': [user['user_email_encoded']] * len(future_dates),
                'user_role_encoded': [user['user_role_encoded']] * len(future_dates),
                'day_of_week': future_dates.dayofweek,
                'month': future_dates.month,
                'previous_overtime_30d': [previous_overtime_30d] * len(future_dates)
            })

            future_df = future_df[future_df['day_of_week'] < 5]
            
            total_overtime_minutes = 0
            if not future_df.empty:
                predictions = self.model.predict(future_df[self.features])
                total_overtime_minutes = predictions.sum()
            
            user_predictions[user['user_email']] = {
                "name": user['user_name'],
                "role": user['user_role'].capitalize(),
                "overtimeMinutes": round(total_overtime_minutes, 2)
            }

        predictions = sorted(user_predictions.values(), key=lambda x: x['overtimeMinutes'], reverse=True)
        return predictions