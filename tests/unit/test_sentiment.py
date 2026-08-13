from unittest.mock import MagicMock, patch

from src.nlp.sentiment import analyze_sentiment


@patch("src.nlp.sentiment.sentiment_pipeline")
def test_analyze_sentiment_positive(mock_pipeline: MagicMock) -> None:
    # Arrange
    mock_pipeline.return_value = [{"label": "positive", "score": 0.98}]

    # Act
    label, score = analyze_sentiment("Company revenue skyrocketed by 200%")

    # Assert
    assert label == "positive"
    assert score == 0.98
    # Assert the pipeline was called with the truncated string
    mock_pipeline.assert_called_once_with("Company revenue skyrocketed by 200%")


@patch("src.nlp.sentiment.sentiment_pipeline")
def test_analyze_sentiment_negative(mock_pipeline: MagicMock) -> None:
    # Arrange
    mock_pipeline.return_value = [{"label": "negative", "score": 0.95}]

    # Act
    label, score = analyze_sentiment("Stocks plummeted amid bankruptcy fears")

    # Assert
    assert label == "negative"
    assert score == 0.95


def test_analyze_sentiment_empty_string() -> None:
    # Act
    label, score = analyze_sentiment("   ")

    # Assert
    assert label == "neutral"
    assert score == 0.0


@patch("src.nlp.sentiment.sentiment_pipeline", None)
def test_analyze_sentiment_no_model() -> None:
    # Act
    label, score = analyze_sentiment("Some valid text but model is missing")

    # Assert
    assert label == "neutral"
    assert score == 0.0


@patch("src.nlp.sentiment.sentiment_pipeline")
def test_analyze_sentiment_exception(mock_pipeline: MagicMock) -> None:
    # Arrange: make the pipeline throw an exception during inference
    mock_pipeline.side_effect = Exception("Model inference failed")

    # Act
    label, score = analyze_sentiment("Valid text that causes a crash")

    # Assert
    assert label == "neutral"
    assert score == 0.0
