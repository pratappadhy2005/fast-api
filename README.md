# 🚀 FastAPI Projects Collection

Welcome to the FastAPI Projects repository! This collection demonstrates a progression from basic FastAPI concepts to deploying Machine Learning models with production-grade practices.

## 📂 Project Modules

This repository is organized into four main modules, each covering different aspects of FastAPI development:

### [01-Basic](./01-Basic)
A fundamental introduction to FastAPI.
- **Key Concepts**: Basic routing, GET endpoints, returning JSON responses.
- **Entry Point**: `main.py`

### [02-CRUD-Operations](./02-CRUD-Operations)
Focuses on Data Validation and Pydantic Models.
- **Key Concepts**: 
  - Advanced Pydantic validation (`Field`, `min_length`, `gt`, `lt`).
  - Computed fields (e.g., auto-calculating BMI and Health Verdict).
  - Handling complex data structures.
- **Entry Point**: `main.py`

### [03-ML-Models](./03-ML-Models)
A full-stack Machine Learning application.
- **Use Case**: Insurance Premium Prediction.
- **Backend**: FastAPI app serving a pre-trained ML model (`pickle`).
- **Frontend**: Interactive **Streamlit** dashboard consuming the API.
- **Data**: Includes Jupyter notebook for model training.
- **Entry Point**: `app.py` (Backend), `frontend.py` (Frontend).

### [04-IMPROVED-API](./04-IMPROVED-API)
A refactored, production-ready version of the ML project.
- **Key Improvements**:
  - **Modular Architecture**: Code split into `config`, `model`, and `schema`.
  - **Dockerization**: Full container support with `Dockerfile`.
  - **Health Checks**: Dedicated endpoints for monitoring (`/health`).
  - **Robust Error Handling**: Improved exception management.
- **Entry Point**: `app.py`

---

## 🛠️ Getting Started

### Prerequisites
- Python 3.10 or higher
- Pip

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/pratappadhy2005/fast-api.git
   cd fast-api
   ```

2. **Create a Virtual Environment** (Recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   Dependencies are listed in `requirements.txt` (specifically in module 04, but widely applicable).
   ```bash
   pip install -r 04-IMPROVED-API/requirements.txt
   ```
   *Note: If you plan to run the Streamlit frontend in module 03, ensure streamlit is installed:*
   ```bash
   pip install streamlit
   ```

---

## 🚀 How to Run

### Running Basic Examples (01 & 02)
Navigate to the directory and start the server:
```bash
cd 01-Basic
uvicorn main:app --reload
```
*Access docs at: `http://localhost:8000/docs`*

### Running the ML Application (03)
**Start the Backend:**
```bash
cd 03-ML-Models
uvicorn app:app --reload
```

**Start the Frontend (in a new terminal):**
```bash
cd 03-ML-Models
streamlit run frontend.py
```

### Running the Improved API (04)
**Local Development:**
```bash
cd 04-IMPROVED-API
uvicorn app:app --reload
```

**Using Docker:**
```bash
cd 04-IMPROVED-API
docker build -t insurance-api .
docker run -p 8000:8000 insurance-api
```

---

## 📚 Tech Stack
- **Framework**: FastAPI
- **Validation**: Pydantic v2
- **Machine Learning**: Scikit-Learn, Pandas, Numpy
- **Frontend**: Streamlit
- **Containerization**: Docker
- **Server**: Uvicorn

---
