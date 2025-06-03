import pandas as pd
from sklearn.ensemble import IsolationForest
import pickle

# Simulate normal speed data
data = pd.DataFrame({"speed": [60, 65, 70, 75, 80, 85, 90, 95, 100] * 20})

# Train anomaly detection model
model = IsolationForest(contamination=0.1)
model.fit(data)

# Save the model
with open("ml_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model saved as ml_model.pkl")
