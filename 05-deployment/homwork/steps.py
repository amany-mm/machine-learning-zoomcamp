# ============================================================================

# HOMEWORK 5: DEPLOYMENT

# ============================================================================

# ============================================================================

# QUESTION 1: Install uv

# ============================================================================

"""
Step 1: Install uv (Python package manager)
`curl -LsSf https://astral.sh/uv/install.sh | sh`

Check version:
`uv --version`

Step 2: Initialize empty uv project

```
mkdir 05-deployment
cd 05-deployment
uv python install 3.13
uv init
```

This creates:

- pyproject.toml
- .python-version
- uv.lock (after first install)
  """

""" Check uv version:
$ uv --version
"""
# ============================================================================

# QUESTION 2: Install Scikit-Learn 1.6.1

# ============================================================================

"""
Install Scikit-Learn version 1.6.1 using uv:
`uv add scikit-learn==1.6.1

This will:

1. Add scikit-learn to pyproject.toml
2. Create/update uv.lock file with dependencies

Check the uv.lock file:
`cat uv.lock | grep -A 5 "name = \"scikit-learn\""`

Look for the first hash starting with sha256:
It should look something like:
sha256:abc123...

The answer of the question 2, the FULL hash string including "sha256:"
"""

# ============================================================================

# QUESTION 3: Load Model and Score

# ============================================================================

import pickle
import requests


def load_and_score_q3():
    """
    Question 3: Load pipeline and score a client
    """
    # First, download the model # wget https://github.com/DataTalksClub/machine-learning-zoomcamp/raw/refs/heads/master/cohorts/2025/05-deployment/pipeline_v1.bin
    # Verify checksum (optional but recommended)
    # md5sum pipeline_v1.bin
    # Should be: 7d17d2e4dfbaf1e408e1a62e6e880d49

    # Load the pipeline
    with open('pipeline_v1.bin', 'rb') as f:
        pipeline = pickle.load(f)

        # Client to score
        client = {
            "lead_source": "paid_ads",
            "number_of_courses_viewed": 2,
            "annual_income": 79276.0
        }

        # Score the client
        # Note: pipeline expects a list of dictionaries
        probability = pipeline.predict_proba([client])[0, 1]

        print(f"Question 3 Answer:")
        print(f"Probability of conversion: {probability:.3f}")
        print(f"Closest option: {round(probability, 3)}")

        return probability

# ============================================================================

# QUESTION 4: FastAPI Service

# ============================================================================


"""
Step 1: Install FastAPI, uvicorn and requests
`uv add fastapi uvicorn requests pydantic`

Step 2: Create serve.py (see code below)

Step 3: Run the service
`uvicorn serve:app --reload --host 0.0.0.0 --port 8000`

Step 4: Test with requests
"""

# ============================================================================

# FILE: serve.py

# ============================================================================

SERVE_PY_CONTENT = '''
from fastapi import FastAPI
import pickle
from pydantic import BaseModel

# Load the model once at startup

with open("pipeline_v1.bin", "rb") as f:
    pipeline = pickle.load(f)

app = FastAPI()

# Define request model

class Lead(BaseModel):
lead_source: str
number_of_courses_viewed: int
annual_income: float

@app.get("/")
def read_root():
return {"message": "Lead Scoring API"}

@app.post("/predict")
def predict(lead: Lead): # Convert to dictionary
lead_dict = lead.dict()

    # Get prediction probability
    probability = pipeline.predict_proba([lead_dict])[0, 1]

    return {
        "conversion_probability": float(probability),
        "will_convert": bool(probability >= 0.5)
    }

'''


def test_fastapi_q4():

"""
Question 4: Test FastAPI service
"""
url = "http://localhost:8000/predict"

client = {
    "lead_source": "organic_search",
    "number_of_courses_viewed": 4,
    "annual_income": 80304.0
}

response = requests.post(url, json=client)
result = response.json()

print(f"\nQuestion 4 Answer:")
print(f"Response: {result}")
print(f"Probability: {result['conversion_probability']:.3f}")

return result

# ============================================================================

# QUESTION 5: Docker Base Image Size

# ============================================================================

"""
Step 1: Pull the base image
docker pull agrigorev/zoomcamp-model:2025

Step 2: Check image size
`$docker images`

Look for agrigorev/zoomcamp-model:2025 in the list
The SIZE column will show the answer

output:
REPOSITORY TAG IMAGE ID CREATED SIZE
agrigorev/zoomcamp-model 2025 abc123def456 2 days ago 121 MB

"""

# ============================================================================

# QUESTION 6: Complete Dockerfile

# ============================================================================

"""
Create a Dockerfile in your homework directory:
"""

DOCKERFILE_CONTENT = '''FROM agrigorev/zoomcamp-model:2025

# Set working directory

WORKDIR /code

# Copy dependency files

COPY pyproject.toml ./

# Install uv

RUN pip install uv

# Install dependencies from pyproject.toml

RUN uv pip install --system -r pyproject.toml

# Copy the FastAPI application

COPY serve.py .

# Expose port

EXPOSE 8000

# Run the application

CMD ["uvicorn", "serve:app", "--host", "0.0.0.0", "--port", "8000"]
'''


"""
For Question 6, modify serve.py to use pipeline_v2.bin
since the Docker image contains pipeline_v2.bin
modify Dockerfile to copy serve_v2.py as serve.py

"""

SERVE_V2_PY = '''
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

'''

"""
# Set working directory

Step 1: Build the image
docker build - t lead-scoring-service .

Step 2: Run the container
docker run - p 8000: 8000 lead-scoring-service

Step 3: Test the endpoint
"""

'''
def test_docker_service_q6():
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

    return result

'''
