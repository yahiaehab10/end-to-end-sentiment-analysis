"""
FastAPI application for sentiment analysis model serving.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Any
import joblib
import pandas as pd
import numpy as np
import logging
import os
from datetime import datetime
import mlflow
import mlflow.sklearn
from contextlib import asynccontextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables for model and vectorizer
model = None
vectorizer = None
model_version = None


class PredictionRequest(BaseModel):
    text: str = Field(..., description="Text to analyze for sentiment", min_length=1)


class BatchPredictionRequest(BaseModel):
    texts: List[str] = Field(
        ..., description="List of texts to analyze", min_items=1, max_items=100
    )


class PredictionResponse(BaseModel):
    text: str
    sentiment: int = Field(
        ..., description="Predicted sentiment: -1 (negative), 0 (neutral), 1 (positive)"
    )
    confidence: float = Field(..., description="Model confidence score")
    timestamp: str


class BatchPredictionResponse(BaseModel):
    predictions: List[PredictionResponse]
    total_count: int


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    model_version: str
    timestamp: str


def load_model_artifacts():
    """Load model and vectorizer artifacts."""
    global model, vectorizer, model_version

    try:
        # Try to load from MLflow first
        if os.getenv("MLFLOW_MODEL_URI"):
            model_uri = os.getenv("MLFLOW_MODEL_URI")
            model = mlflow.sklearn.load_model(model_uri)
            model_version = "mlflow_latest"
            logger.info(f"Loaded model from MLflow: {model_uri}")
        else:
            # Fallback to local files
            model_path = "lgbm_model.pkl"
            vectorizer_path = "tfidf_vectorizer.pkl"

            if os.path.exists(model_path) and os.path.exists(vectorizer_path):
                model = joblib.load(model_path)
                vectorizer = joblib.load(vectorizer_path)
                model_version = "local_v1.0"
                logger.info("Loaded model and vectorizer from local files")
            else:
                raise FileNotFoundError("Model artifacts not found")

    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        raise


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Loading model artifacts...")
    load_model_artifacts()
    logger.info("Model loaded successfully")
    yield
    # Shutdown
    logger.info("Shutting down...")


# Create FastAPI app
app = FastAPI(
    title="Sentiment Analysis API",
    description="API for sentiment analysis using machine learning",
    version="1.0.0",
    lifespan=lifespan,
)


def preprocess_text(text: str) -> str:
    """Basic text preprocessing."""
    import re

    # Convert to lowercase
    text = text.lower()

    # Remove URLs
    text = re.sub(r"http\S+|www\S+|https\S+", "", text, flags=re.MULTILINE)

    # Remove user mentions and hashtags
    text = re.sub(r"@\w+|#\w+", "", text)

    # Remove extra whitespace
    text = " ".join(text.split())

    return text


def predict_sentiment(text: str) -> Dict[str, Any]:
    """Predict sentiment for a single text."""
    if model is None or vectorizer is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    try:
        # Preprocess text
        processed_text = preprocess_text(text)

        # Vectorize text
        text_vector = vectorizer.transform([processed_text])

        # Make prediction
        prediction = model.predict(text_vector)[0]

        # Get prediction probabilities for confidence score
        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(text_vector)[0]
            confidence = float(np.max(probabilities))
        else:
            confidence = 0.5  # Default confidence if probabilities not available

        return {
            "text": text,
            "sentiment": int(prediction),
            "confidence": confidence,
            "timestamp": datetime.utcnow().isoformat(),
        }

    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail="Prediction failed")


@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint."""
    return {"message": "Sentiment Analysis API", "version": "1.0.0"}


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status=(
            "healthy" if model is not None and vectorizer is not None else "unhealthy"
        ),
        model_loaded=model is not None and vectorizer is not None,
        model_version=model_version or "unknown",
        timestamp=datetime.utcnow().isoformat(),
    )


@app.post("/predict", response_model=PredictionResponse)
async def predict_single(request: PredictionRequest):
    """Predict sentiment for a single text."""
    result = predict_sentiment(request.text)
    return PredictionResponse(**result)


@app.post("/predict/batch", response_model=BatchPredictionResponse)
async def predict_batch(request: BatchPredictionRequest):
    """Predict sentiment for multiple texts."""
    predictions = []

    for text in request.texts:
        try:
            result = predict_sentiment(text)
            predictions.append(PredictionResponse(**result))
        except Exception as e:
            logger.error(f"Failed to predict for text: {text[:50]}... Error: {e}")
            # Continue with other texts, or you can choose to fail the entire batch
            continue

    return BatchPredictionResponse(
        predictions=predictions, total_count=len(predictions)
    )


@app.get("/model/info", response_model=Dict[str, Any])
async def get_model_info():
    """Get model information."""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    info = {
        "model_type": type(model).__name__,
        "model_version": model_version,
        "loaded_at": datetime.utcnow().isoformat(),
        "features_expected": (
            getattr(vectorizer, "vocabulary_", {}) if vectorizer else "unknown"
        ),
    }

    # Add model-specific info if available
    if hasattr(model, "feature_importances_"):
        info["has_feature_importances"] = True

    return info


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")

    uvicorn.run("main:app", host=host, port=port, reload=False, log_level="info")
