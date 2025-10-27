"""
For Question 6, you'll need to modify serve.py to use pipeline_v2.bin
since the Docker image contains pipeline_v2.bin


# ============================================================================
# Build and run Docker container:
Step 1: Build the image
docker build - t lead-scoring-service .

Step 2: Run the container
docker run - p 8000: 8000 lead-scoring-service

Step 3: Test the endpoint
"""


from fastapi import FastAPI
import pickle
from pydantic import BaseModel

# Load pipeline_v2.bin (already in the base image)
with open("pipeline_v2.bin", "rb") as f:
    pipeline = pickle.load(f)

app = FastAPI()


class Lead(BaseModel):
    lead_source: str
    number_of_courses_viewed: int
    annual_income: float


@app.get("/")
def read_root():
    return {"message": "Lead Scoring API v2"}


@app.post("/predict")
def predict(lead: Lead):
    lead_dict = lead.dict()
    probability = pipeline.predict_proba([lead_dict])[0, 1]

    return {
        "conversion_probability": float(probability),
        "will_convert": bool(probability >= 0.5)
    }
