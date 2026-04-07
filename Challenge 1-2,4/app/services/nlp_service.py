from transformers import pipeline
import re

COMMON_OBJECTS = [
    # COCO classes
    "person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck",
    "boat", "traffic light", "fire hydrant", "stop sign", "parking meter", "bench",
    "bird", "cat", "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra",
    "giraffe", "backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee",
    "skis", "snowboard", "sports ball", "kite", "baseball bat", "baseball glove",
    "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
    "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange",
    "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair", "couch",
    "potted plant", "bed", "dining table", "toilet", "tv", "laptop", "mouse",
    "remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "sink",
    "refrigerator", "book", "clock", "vase", "scissors", "teddy bear",
    "hair drier", "toothbrush", "panda",
    "gun", "weapon", "rifle", "pistol", "sword", "helmet", "badge", "uniform"
]

# Sentiment Analysis
sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

# Semantic Mapping
semantic_classifier = pipeline(
    "zero-shot-classification",
    model="typeform/distilbert-base-uncased-mnli"
)

# Keyword Extraction
ner_pipeline = pipeline("ner", aggregation_strategy="simple")


def clean_text(text: str) -> str:
    """Basic text cleaning for better pipeline processing."""
    return text.strip().replace("\n", " ")


def is_generic_query(text: str) -> bool:
    """Detect if the query is generic (e.g., 'what is this?', 'what do you see?')."""
    generic_patterns = [
        r"\bwhat is\b", r"\bwhat are\b", r"\bwhat do you see\b",
        r"\bdescribe\b", r"\bidentify\b", r"\bdetect\b", r"\bfind\b",
        r"\bwhat's in\b", r"\btell me\b", r"\bshow me\b", r"\blook at\b"
    ]
    return any(re.search(p, text.lower()) for p in generic_patterns)


def extract_keywords(text: str) -> list:
    """
    Extracts relevant keywords from text using a Transformer-based NER model.
    Falls back to content words if no entities found.
    """
    cleaned = clean_text(text)
    if not cleaned:
        return []

    entities = ner_pipeline(cleaned)
    keywords = [ent['word'].strip() for ent in entities if 'word' in ent]

    if not keywords:
        words = re.findall(r'\b\w{3,}\b', cleaned.lower())
        stop_words = {'the', 'and', 'with', 'for', 'this', 'that', 'they', 'from',
                      'what', 'does', 'there', 'here', 'how', 'who', 'why', 'when',
                      'are', 'was', 'were', 'been', 'being', 'have', 'has', 'had',
                      'can', 'could', 'will', 'would', 'shall', 'should', 'may',
                      'might', 'must', 'you', 'see', 'any', 'some',
                      'holding', 'running', 'walking', 'sitting', 'standing',
                      'looking', 'using', 'carrying', 'wearing', 'playing',
                      'eating', 'drinking', 'driving', 'riding', 'throwing'}
        keywords = [w for w in words if w not in stop_words][:5]

    return list(set(keywords))


def map_query_to_classes(text: str) -> list:
    """
    Maps a text query to detectable object class names.
    - Generic queries ('what is this?') -> use ALL common classes
    - Specific queries ('is this a living being?') -> zero-shot classification
    """
    if is_generic_query(text):
        return COMMON_OBJECTS

    result = semantic_classifier(
        text,
        candidate_labels=COMMON_OBJECTS,
        multi_label=True,
        hypothesis_template="This is a photo of a {}."
    )

    matched = [
        label for label, score in zip(result["labels"], result["scores"])
        if score > 0.4
    ][:5]

    if not matched:
        matched = result["labels"][:1]

    return matched


def analyze_text(text: str) -> dict:
    """
    Main entry point for text analysis.
    Returns keywords, semantically mapped classes, and sentiment.
    """
    cleaned = clean_text(text)
    if not cleaned:
        return {"keywords": [], "semantic_classes": [], "sentiment": "NEUTRAL"}

    sentiment = sentiment_pipeline(cleaned)[0]
    keywords = extract_keywords(cleaned)
    semantic_classes = map_query_to_classes(cleaned)

    return {
        "keywords": keywords,
        "semantic_classes": semantic_classes,
        "sentiment": sentiment["label"]
    }