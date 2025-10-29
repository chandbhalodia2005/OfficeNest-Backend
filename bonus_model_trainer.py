# bonus_model_trainer.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib
import os

# --- 1. Simulate Historical Data ---
data = {
    'punctuality_score': [95, 80, 70, 90, 60, 85, 75, 92, 65, 88],
    'late_score': [5, 20, 30, 10, 40, 15, 25, 8, 35, 12],
    'absent_score': [2, 10, 15, 5, 25, 8, 12, 3, 20, 6],
    'overtime_score': [80, 70, 60, 85, 50, 75, 65, 90, 55, 82],
    'actual_bonus_score': [92.5, 75.0, 65.0, 88.0, 55.0, 80.0, 70.0, 91.5, 60.0, 85.5]
}
df = pd.DataFrame(data)

# --- 2. Prepare Data and Train the Model ---
features = ['punctuality_score', 'late_score', 'absent_score', 'overtime_score']
target = 'actual_bonus_score'

X = df[features]
y = df[target]

model = LinearRegression()
model.fit(X, y)

# --- 3. Save the Trained Model ---
model_filename = 'bonus_prediction_model.joblib'
joblib.dump(model, model_filename)

print(f"Model saved as {model_filename}")