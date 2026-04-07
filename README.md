# Project Multimodal: The Intelligent Service Orchestrator

<div align="center">

[![Backend - Challenge 1-2,4](https://img.shields.io/badge/Backend-Challenge%201--2%2C4-blue?style=for-the-badge&logo=python&logoColor=white)](./Challenge%201-2,4)
[![Frontend - Challenge 3](https://img.shields.io/badge/Frontend-Challenge%203-61DAFB?style=for-the-badge&logo=react&logoColor=black)](./Challenge%203)

</div>

## Overview

As an applicant for the **Intern AI Software Engineer** role at **Limi AI**, this project serves as a bridge between academic model development and production-grade software engineering. This repository contains the complete implementation of the AI Engineering Challenge, evolving a research-based prototype into a scalable, user-facing application.

---

## Repository Structure

This project is divided into two main components:

### 🔹 [Backend - Challenge 1, 2, & 4](./Challenge%201-2,4)
The core intelligence layer of the system.
- **Challenge 1**: Hybrid Inference Engine (YOLOv26 + DistilBERT).
- **Challenge 2**: Production-Grade FastAPI with Docker, DVC, and MLflow integration.
- **Challenge 4**: High-performance LRU Cache (Hash Map + Doubly Linked List) for minimized latency.
- **Check the [Backend README](./Challenge%201-2,4/README.md) for technical details.**

### 🔹 [Frontend - Challenge 3](./Challenge%203)
The interactive user interface.
- **Challenge 3**: Responsive React/Vite application for real-time visualization of bounding boxes and NLP analysis.
- **Architecture**: Includes a clean, modern design with glassmorphism and smooth transitions.
- **Documents**: Check the `docs/` folder for UI wireframes and component hierarchy.
- **Check the [Frontend README](./Challenge%203/limiai-fe/README.md) for setup instructions.**

---

## 🚀 The Challenges implementation

### **Challenge 1: The Hybrid Inference Engine** (Core Skills - 30%)
Utilizing demonstrated hands-on experience in both Computer Vision and Natural Language Processing, this Python-based service accepts an image and a text query. The service uses an OpenCV/PyTorch pipeline to perform object detection on the image and a Transformer-based model (DistilBERT) to extract relevant keywords and sentiment.

### **Challenge 2: Production-Grade API & Deployment** (Addressing Gaps - 20%)
Created a RESTful API using **FastAPI** to serve models. The application is fully containerized using **Docker**. It addresses exposure to major Cloud ML platforms (AWS SageMaker, Google Cloud AI Platform, Azure ML) and incorporates MLOps concepts like model versioning (DVC) and experiment tracking (MLflow).

### **Challenge 3: Frontend Orchestration** (Frontend Requirement - 30%)
Developed a responsive web interface using **React**. The UI allows users to upload images, input text queries, and view processed results (bounding boxes rendered on the image and sentiment labels) with a clean, modern design.

### **Challenge 4: Algorithmic Efficiency** (Core Skills - 20%)
Implemented an **LRU Cache** using a **Hash Map + Doubly Linked List**. This choice optimizes latency in a production environment by ensuring $O(1)$ operations for both retrieval and updates, significantly reducing compute costs for repeat queries.

