# ============================================================================
# QUESTION 4: FastAPI Service
# ============================================================================

"""
Step 1: Install FastAPI and uvicorn
uv add fastapi uvicorn

Step 2: Create serve.py (see code below)

Step 3: Run the service
uvicorn serve:app --reload --host 0.0.0.0 --port 8000

Step 4: Test with requests
"""


from fastapi import FastAPI
import pickle
from pydantic import BaseModel

# Load the model
with open("pipeline_v1.bin", "rb") as f:
    pipeline = pickle.load(f)

app = FastAPI()


class Lead(BaseModel):
    lead_source: str
    number_of_courses_viewed: int
    annual_income: float


@app.post("/predict")
def predict(lead: Lead):
    lead_dict = lead.dict()
    probability = pipeline.predict_proba([lead_dict])[0, 1]
    return {"conversion_probability": float(probability)}
