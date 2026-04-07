# LimiAI-Assesment 🧠✨

An advanced, responsive web interface for real-time image analysis and semantic intelligence. Built with **React 19** and **Vite**, this application provides a premium user experience for visualizing object detection and natural language processing results.

---

## 🌟 Key Features

- **Premium UI/UX**: Modern dark-themed interface with glassmorphism effects and smooth transitions.
- **Interactive Image Analysis**:
    - **Dynamic Bounding Boxes**: Visualize detected objects with real-time SVG overlays, including labels and confidence scores.
    - **Sentiment Intelligence**: Instant sentiment analysis of user queries (POSITIVE, NEGATIVE, NEUTRAL).
    - **Semantic Insights**: Detailed keyword extraction and semantic mapping of detections.
- **Robust Integration**:
    - Fully configurable API base URL via environment variables.
    - Seamless multipart/form-data handling for high-resolution image uploads.
    - Real-time loading states and graceful error handling.
- **Fully Responsive**: Optimized for desktop, tablet, and mobile viewing.

---

## 🛠️ Technology Stack

- **Framework**: [React 19](https://react.dev/)
- **Build Tool**: [Vite 8](https://vitejs.dev/)
- **Styling**: Vanilla CSS (Custom Design System)
- **Icons**: [Lucide React](https://lucide.dev/)
- **State Management**: React Hooks (useState, useEffect, useRef)
- **API Communication**: Native Fetch API

---

## 📂 Project Structure

```text
limiai-fe/
├── src/
│   ├── components/
│   │   ├── AnalysisDisplay.jsx  # SVG-powered visualization & results
│   │   └── ImageUpload.jsx      # Drag-and-drop file handling
│   ├── App.jsx                  # Main application & API logic
│   ├── index.css                # Global design system & variables
│   └── main.jsx                 # Application entry point
├── .env                         # API configuration
├── package.json                 # Dependency management
└── vite.config.js               # Build configuration
```

---

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have [Node.js](https://nodejs.org/) (v18+) and [npm](https://www.npmjs.com/) installed.

### 2. Installation
Clone the repository and install the dependencies:
```bash
git clone <repository-url>
cd limiai-fe
npm install
```

### 3. Configuration
Create or update the `.env` file in the root directory:
```env
VITE_API_BASE_URL=http://localhost:9000
```

### 4. Development
Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:5173`.

---

## 🔗 API Integration

The frontend expects a backend service running at `VITE_API_BASE_URL` with a POST endpoint `/analyze`:

**Request:**
- **Method**: `POST`
- **Content-Type**: `multipart/form-data`
- **Body**: 
    - `image`: (File) The image to analyze.
    - `text`: (String) The query for text analysis.

**Response Schema:**
```json
{
  "status": "success",
  "data": {
    "detected_objects": [
      {
        "label": "string",
        "confidence": number,
        "box": [x1, y1, x2, y2]
      }
    ],
    "text_analysis": {
      "query": "string",
      "sentiment": "string",
      "extracted_keywords": ["string"],
      "semantic_mapping": ["string"]
    }
  }
}
```

---

## 📐 Architecture & Design

For a detailed breakdown of the UI structure, data flow, and design principles, please refer to the [Component Hierarchy Documentation](file:///home/amman/Data/limiai/Challenge%203/limiai-fe/docs/component_hierarchy.md).

---

## 🎨 Design System

This project uses a custom-built Vanilla CSS design system focused on performance and aesthetics:
- **Primary Color**: `#8b5cf6` (Soft Purple)
- **Background**: `#0f172a` (Slate Dark)
- **Typography**: Inter (System-ui fallback)
- **Glassmorphism**: 12px blur with 3% white overlay.

---



<p align="center">
  Developed with ❤️ for the LimiAI Assessment.
</p>
