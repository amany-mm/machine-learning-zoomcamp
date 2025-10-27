import requests

response = requests.post(
    'http://localhost:8000/predict',
    json={
        'lead_source': 'organic_search',
        'number_of_courses_viewed': 4,
        'annual_income': 80304.0
    }
)

result = response.json()
prob = result['conversion_probability']

print("="*50)
print(f"Probability: {prob:.3f}")

# Find closest answer
options = [0.334, 0.534, 0.734, 0.934]
closest = min(options, key=lambda x: abs(x - prob))
print(f"Closest option: {closest}")
print("="*50)
