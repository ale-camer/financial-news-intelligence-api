import spacy

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")


def extract_entities(text: str) -> list[dict[str, str]]:
    """
    Extract relevant financial entities (ORG, PERSON, GPE, MONEY) from text.

    Args:
        text (str): The text to process.

    Returns:
        list[dict[str, str]]: A list of unique entities and their labels.
    """
    if not text or not text.strip():
        return []

    doc = nlp(text)
    relevant_labels = {"ORG", "PERSON", "GPE", "MONEY"}

    # Use a set to avoid duplicate entities
    unique_entities = set()
    results = []

    for ent in doc.ents:
        if ent.label_ in relevant_labels:
            entity_tuple = (ent.text, ent.label_)
            if entity_tuple not in unique_entities:
                unique_entities.add(entity_tuple)
                results.append({"entity": ent.text, "label": ent.label_})

    return results
