import hashlib
import re


def clean_text(text: str) -> str:
    """
    Remove HTML tags and normalize whitespace in a string.

    Args:
        text: The raw input text.

    Returns:
        The cleaned string.
    """
    if not text:
        return ""

    # Remove HTML tags
    cleaned = re.sub(r"<[^>]+>", "", text)

    # Normalize whitespace (replace multiple spaces/newlines with a single space)
    cleaned = re.sub(r"\s+", " ", cleaned)

    return cleaned.strip()


def generate_content_hash(text: str) -> str:
    """
    Generate a SHA-256 hex digest for the given text.

    Args:
        text: The cleaned text.

    Returns:
        The SHA-256 hex digest string.
    """
    if not text:
        return hashlib.sha256(b"").hexdigest()

    return hashlib.sha256(text.encode("utf-8")).hexdigest()
