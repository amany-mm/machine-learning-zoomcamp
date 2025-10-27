FROM agrigorev/zoomcamp-model:2025

# Set working directory
WORKDIR /code

# Copy dependency files
COPY pyproject.toml ./

# Install uv
RUN pip install uv

# Install dependencies from pyproject.toml
RUN uv pip install --system -r pyproject.toml

# Copy the FastAPI application
COPY serve_v2.py .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "serve_v2:app", "--host", "0.0.0.0", "--port", "8000"]