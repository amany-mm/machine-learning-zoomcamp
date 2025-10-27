import requests

"""
    Question 6: Test Docker service
    """
url = "http://localhost:8000/predict"

client = {
    "lead_source": "organic_search",
    "number_of_courses_viewed": 4,
    "annual_income": 80304.0
}

response = requests.post(url, json=client)
result = response.json()

print(f"\nQuestion 6 Answer:")
print(f"Response: {result}")
print(f"Probability: {result['conversion_probability']:.3f}")
