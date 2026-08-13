import logging

from typing import Any

from transformers import pipeline

logger = logging.getLogger(__name__)

# Initialize the model at the module level to avoid loading it on every call.
# ProsusAI/finbert is pre-trained specifically on financial text.
try:
    sentiment_pipeline: Any = pipeline("text-classification", model="ProsusAI/finbert")
except Exception as e:
    logger.error(f"Failed to load FinBERT model: {e}")
    sentiment_pipeline = None


def analyze_sentiment(text: str) -> tuple[str, float]:
    """
    Analyzes the sentiment of a given financial text using FinBERT.
    Returns a tuple of (sentiment_label, confidence_score).
    If the text is empty or the model failed to load, returns ("neutral", 0.0).
    """
    if not text or not text.strip():
        return ("neutral", 0.0)

    if sentiment_pipeline is None:
        logger.warning("Sentiment pipeline is not loaded. Returning neutral.")
        return ("neutral", 0.0)

    try:
        # Truncate text roughly to avoid BERT token limits (usually 512 tokens).
        # In a production environment with very long articles, we would use a proper
        # tokenizer or sliding window approach.
        truncated_text = text[:1500]
        result = sentiment_pipeline(truncated_text)

        # Result is typically a list of dicts: [{'label': 'positive', 'score': 0.95}]
        if result and isinstance(result, list):
            best_prediction = result[0]
            label = best_prediction.get("label", "neutral").lower()
            score = float(best_prediction.get("score", 0.0))
            return (label, score)

        return ("neutral", 0.0)
    except Exception as e:
        logger.error(f"Error during sentiment analysis: {e}")
        return ("neutral", 0.0)
