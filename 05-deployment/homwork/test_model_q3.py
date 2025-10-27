import pickle

# Load model
with open('pipeline_v1.bin', 'rb') as f:
    pipeline = pickle.load(f)

# Test data
client = {
    "lead_source": "paid_ads",
    "number_of_courses_viewed": 2,
    "annual_income": 79276.0
}

# Predict
prob = pipeline.predict_proba([client])[0, 1]
print(f"Probability: {prob:.3f}")
