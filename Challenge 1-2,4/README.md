# AI Image Analysis Service 🚀

![AI Service Banner](https://img.shields.io/badge/AI-Image%20Analysis-blue?style=for-the-badge&logo=ai)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![YOLO](https://img.shields.io/badge/YOLO-v26-green?style=for-the-badge&logo=opencv)
![Transformers](https://img.shields.io/badge/Transformers-Hugging%20Face-orange?style=for-the-badge&logo=huggingface)

A robust, production-grade AI service built with **FastAPI** that combines advanced **Object Detection** (YOLOE-26) and **Natural Language Processing** (Transformers) to analyze images based on user queries.

---

## ✨ Features

- **🔍 Open-Vocabulary Object Detection**: Powered by **YOLOE-26**, allowing for detection of arbitrary objects defined by text queries.
- **🧠 Advanced NLP Pipeline**:
  - **Sentiment Analysis**: DistilBERT-based sentiment extraction.
  - **Keyword Extraction**: Transformer-based NER for relevant term identification.
  - **Semantic Mapping**: Zero-Shot classification to map abstract queries to concrete detectable objects.
- **⚡ High-Performance LRU Cache**: Custom implementation using **Hash Map + Doubly Linked List** for $O(1)$ operations, achieving sub-millisecond response times for repeat queries.
- **🐳 Dockerized**: Fully containerized and ready for scalable cloud deployment.
- **🏥 Health Monitoring**: Built-in `/health` endpoints for orchestration tools (K8s, ECS).

---

## 🏗️ Architecture

The service follows a clean, modular architecture:

```text
├── app/
│   ├── api/
│   │   └── routes.py         # API endpoints and request orchestration
│   ├── services/
│   │   ├── yolo_service.py   # Computer Vision (YOLO) logic
│   │   ├── nlp_service.py    # NLP (Sentiment, NER, Zero-Shot) logic
│   │   └── cache_service.py  # Custom LRU Cache implementation
│   └── main.py              # FastAPI application & middleware config
├── Dockerfile               # Multi-stage production build
├── docker-compose.yml       # Local development orchestration
└── pyproject.toml           # Dependency management
```

---

## 🚀 Getting Started

### 📦 Prerequisites
- Python 3.13+
- Docker & Docker Compose (optional)

### 🛠️ Local Installation
1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd challenge-1-2
   ```

2. **Set up virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   # or
   .venv\Scripts\activate     # Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -e .
   ```

4. **Run the server:**
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 9000
   ```

### 🐳 Running with Docker
```bash
docker-compose up --build
```
The service will be available at `http://localhost:9000`.

---

## 📡 API Documentation

### **POST** `/analyze`
Analyzes an image based on a text prompt.

**Request:**
- `Content-Type: multipart/form-data`
- `image`: File (JPEG/PNG)
- `text`: String (Query prompt)

**Example Curl:**
```bash
curl -X 'POST' \
  'http://localhost:9000/analyze' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'image=@photo.jpg;type=image/jpeg' \
  -F 'text=a man holding a gun'
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "detected_objects": [
      {
        "label": "person",
        "confidence": 0.95,
        "box": [322, 124, 838, 1471]
      }
    ],
    "text_analysis": {
      "query": "a man holding a gun",
      "sentiment": "NEGATIVE",
      "extracted_keywords": ["gun", "man"],
      "semantic_mapping": ["person", "weapon"]
    }
  },
  "cached": false
}
```

---

## ⚡ Performance Optimization: LRU Cache

To ensure production-grade latency, we implemented a custom **LRU (Least Recently Used) Cache** found in `app/services/cache_service.py`.

### **Design Choice: Hash Map + Doubly Linked List**
- **Hash Map (Python Dict)**: Provides **O(1)** average-time lookups to find if a combination of image and text has already been processed.
- **Doubly Linked List**: Maintains the "recency" of items. Adding to the head, moving nodes, and evicting the tail (Least Recently Used) are all **O(1)** operations.
- **Impact**: Inference results are cached by a hash of the image content and the query string. Repeat requests bypass the heavy GPU/CPU compute, returning results in **< 1ms**.

---

## 🛠️ MLOps & Production Readiness

This project implements industry-standard MLOps practices for model versioning and experiment tracking.

### **1. 📊 Experiment Tracking (MLflow)**
We use **MLflow** to track every inference request, following MLOps best practices for monitoring and reproducibility:
- **Metrics**: Latency (ms), confidence scores, and detection counts.
- **Parameters**: Text queries, extraction parameters, and model hyperparameters.
- **Tags**: Model versions (YOLOv26, DistilBERT), environment (dev/prod), and sentiment labels.
- **Access**: Integrated with local `mlruns` or remote Databricks/Managed MLflow servers.

### **2. 📦 Model Versioning (DVC)**
Model weights are not stored in Git. Instead, we use **DVC (Data Version Control)** to ensure:
- **Reproducibility**: `dvc.yaml` defines the lineage from raw weights to validated production artifacts.
- **Integrity**: MD5/SHA validation of large binary files (`.pt`, `.ts`) during CI/CD.
- **Storage**: Seamless integration with S3, GCS, or Azure Blob Storage via `dvc remote`.

### **3. 🤖 CI/CD Pipeline**
Our **GitHub Actions** workflow automates:
- **Linting & Testing**: Python 3.13 verification.
- **MLOps Validation**: Automatic DVC verification.
- **Containerization**: Multi-stage production Docker builds (<1.5GB).
- **Push & Deploy**: Automated generic deployment steps.
