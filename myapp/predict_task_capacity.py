import json
import sys

def predict_capacity(employee_data):
    """
    Simulates a machine learning model to predict employee task capacity.
    """
    predictions = []
    
    if not employee_data:
        return predictions

    for employee in employee_data:
        assigned = employee.get('tasks_assigned_last_month', 0)
        completed = employee.get('tasks_completed_last_month', 0)
        
        if assigned == 0:
            capacity_score = 100.0
        else:
            completion_rate = completed / assigned
            capacity_score = completion_rate * 100
            
            if completion_rate >= 0.9:
                capacity_score = min(100.0, capacity_score + 10)
                
        predictions.append({
            "name": employee.get("name", "Unknown"),
            "predicted_capacity": capacity_score
        })
        
    return predictions

if __name__ == "__main__":
    # Read the JSON input from standard input
    try:
        input_json = sys.stdin.read()
        if input_json:
            data = json.loads(input_json)
            employee_data = data.get('employee_data', [])
            result = predict_capacity(employee_data)
            print(json.dumps(result))
    except Exception as e:
        # Print the error to standard error for debugging
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)