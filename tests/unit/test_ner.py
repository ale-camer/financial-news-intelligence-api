from src.nlp.ner import extract_entities


def test_extract_entities_standard() -> None:
    text = "Tim Cook announced that Apple is opening a new office in London."
    entities = extract_entities(text)

    # We expect Tim Cook (PERSON), Apple (ORG), London (GPE)
    assert {"entity": "Tim Cook", "label": "PERSON"} in entities
    assert {"entity": "Apple", "label": "ORG"} in entities
    assert {"entity": "London", "label": "GPE"} in entities


def test_extract_entities_money() -> None:
    text = "The company raised $1.5 billion in funding."
    entities = extract_entities(text)

    assert {"entity": "$1.5 billion", "label": "MONEY"} in entities


def test_extract_entities_empty_string() -> None:
    assert extract_entities("") == []
    assert extract_entities("   ") == []


def test_extract_entities_duplicates() -> None:
    text = "Apple is great. Apple makes phones."
    entities = extract_entities(text)

    # Should only contain one Apple entity
    apple_entities = [e for e in entities if e["entity"] == "Apple"]
    assert len(apple_entities) == 1
    assert apple_entities[0]["label"] == "ORG"
