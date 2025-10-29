# your_project/your_app/bonus_prediction_model.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import os

def train_and_save_model():
    """
    Trains a RandomForestClassifier model and saves it to a file.
    """
    # 1. Data Preparation (Simulated Data)
    # In a real-world scenario, you would load this from your Django database.
    data = {
        'tasks_completed': [10, 25, 45, 60, 5, 30, 55, 70, 40, 20],
        'on_time_percentage': [80, 95, 98, 92, 60, 85, 99, 90, 88, 75],
        'is_manager': [0, 0, 0, 1, 0, 0, 1, 1, 0, 0],
        'received_bonus': [0, 1, 1, 1, 0, 0, 1, 1, 1, 0] # 1 for bonus, 0 for no bonus
    }
    df = pd.DataFrame(data)

    X = df[['tasks_completed', 'on_time_percentage', 'is_manager']]
    y = df['received_bonus']

    # 2. Model Training
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    model = RandomForestClassifier(n_estimators=10, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate the model (optional but recommended)
    y_pred = model.predict(X_test)
    print(f"Model Accuracy: {accuracy_score(y_test, y_pred):.2f}")

    # 3. Save the Model
    # The model file will be loaded by your Django view for making predictions.
    model_filename = 'bonus_prediction_model.pkl'
    joblib.dump(model, model_filename)
    print(f"Model trained and saved as '{model_filename}'")

def predict_bonus_example(tasks_completed, on_time_percentage, is_manager):
    """
    An example function to test the saved model.
    """
    try:
        loaded_model = joblib.load('bonus_prediction_model.pkl')
        
        new_data = pd.DataFrame(
            [[tasks_completed, on_time_percentage, is_manager]], 
            columns=['tasks_completed', 'on_time_percentage', 'is_manager']
        )
        
        prediction = loaded_model.predict(new_data)
        
        if prediction[0] == 1:
            return "High chance of bonus."
        else:
            return "Low chance of bonus."
    except FileNotFoundError:
        return "Error: Model file not found. Please run the training script first."
    except Exception as e:
        return f"An error occurred during prediction: {e}"

if __name__ == '__main__':
    train_and_save_model()
    print("\n--- Example Predictions ---")
    # A high-performing employee
    print(f"Prediction for a high-performing employee: {predict_bonus_example(tasks_completed=55, on_time_percentage=95, is_manager=0)}")
    # A low-performing employee
    print(f"Prediction for a low-performing employee: {predict_bonus_example(tasks_completed=10, on_time_percentage=65, is_manager=0)}")
    # A high-performing manager
    print(f"Prediction for a high-performing manager: {predict_bonus_example(tasks_completed=70, on_time_percentage=99, is_manager=1)}")