import hashlib

from src.nlp.preprocessing import clean_text, generate_content_hash


def test_clean_text_removes_html() -> None:
    text = "<p>Hello <b>World</b></p>"
    assert clean_text(text) == "Hello World"


def test_clean_text_normalizes_whitespace() -> None:
    text = "  Too   many \n   spaces  "
    assert clean_text(text) == "Too many spaces"


def test_clean_text_empty() -> None:
    assert clean_text("") == ""
    assert clean_text(None) == ""  # type: ignore


def test_generate_content_hash_consistency() -> None:
    text = "This is a test document."
    hash1 = generate_content_hash(text)
    hash2 = generate_content_hash(text)

    assert hash1 == hash2
    assert hash1 == hashlib.sha256(text.encode("utf-8")).hexdigest()


def test_generate_content_hash_differences() -> None:
    text1 = "Document A"
    text2 = "Document B"

    assert generate_content_hash(text1) != generate_content_hash(text2)


def test_generate_content_hash_empty() -> None:
    assert generate_content_hash("") == hashlib.sha256(b"").hexdigest()
