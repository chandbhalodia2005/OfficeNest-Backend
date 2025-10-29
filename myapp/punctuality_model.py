# your_project/your_app/punctuality_model.py

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from datetime import timedelta, datetime

class PunctualityPredictor:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=50, random_state=42)
        self.features = ["total_days", "avg_late", "late_freq", "role_code"]

    def _calculate_punctuality_metrics(self, person, role, attendance_qs):
        if not attendance_qs.exists():
            return None

        df = pd.DataFrame(list(attendance_qs.values("date", "real_entry_time")))
        df["expected_entry_time"] = str(person.shift_start)

        # Calculate late minutes
        df["late_minutes"] = (
            pd.to_datetime(df["real_entry_time"].astype(str), errors="coerce") -
            pd.to_datetime(df["expected_entry_time"].astype(str), errors="coerce")
        ).dt.total_seconds() / 60
        df["late_minutes"] = df["late_minutes"].fillna(0)
        df["is_late"] = (df["late_minutes"] > 0).astype(int)

        total_days = len(df)
        days_present = total_days
        total_workdays = 30  # Assuming a 30-day period for the base calculation
        avg_late = df["late_minutes"].mean()
        late_freq = df["is_late"].mean()

        # Simple scoring formula
        max_allowed_late_minutes = 30
        lateness_penalty = min(avg_late / max_allowed_late_minutes, 1) * 50
        absence_penalty = (1 - (days_present / total_workdays)) * 50

        punctuality_score = round(
            max(0, 100 - (lateness_penalty + absence_penalty)), 2
        )

        return {
            "name": person.name,
            "role": role,
            "total_days": total_days,
            "avg_late": avg_late,
            "late_freq": late_freq,
            "punctuality_score": punctuality_score
        }

    def prepare_data(self, employees, managers, one_month_ago):
        records = []
        for emp in employees:
            attendance_qs = emp.attendance_set.filter(date__gte=one_month_ago)
            result = self._calculate_punctuality_metrics(emp, "Employee", attendance_qs)
            if result:
                records.append(result)

        for mgr in managers:
            attendance_qs = mgr.attendance_set.filter(date__gte=one_month_ago)
            result = self._calculate_punctuality_metrics(mgr, "Manager", attendance_qs)
            if result:
                records.append(result)

        df = pd.DataFrame(records)
        if df.empty:
            return None

        df["role_code"] = np.where(df["role"] == "Manager", 1, 0)
        return df

    def train_and_predict(self, df):
        if df is None or df.empty:
            return None

        X = df[self.features]
        y = df["punctuality_score"]

        # Train the model
        self.model.fit(X, y)

        # Predict using the trained model
        df["predicted_score"] = np.round(self.model.predict(X), 2)
        return df