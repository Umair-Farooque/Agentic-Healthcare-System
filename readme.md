# Agentic Healthcare System

A multi-agent healthcare workflow system powered by LangGraph and OpenAI.

## Overview

This system processes patient intake data (text, PDF, Images) through a sequence of agents:
1. **Intake Agent**: Extracts structured data from raw input.
2. **Validation Agent**: Validates the extracted data.
3. **Reasoning Agent**: Makes clinical decisions based on the data.
4. **Action Agent**: Recommends actions or treatments.
5. **Audit Agent**: Logs the process for compliance.

## Setup

1. **Clone the repository**
2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Install Tesseract OCR**
   - Windows: Download installer from [UB-Mannheim/tesseract](https://github.com/UB-Mannheim/tesseract/wiki)
   - Add Tesseract to your system PATH.

## Configuration

1. Copy `.env.example` to `.env`
   ```bash
   cp .env.example .env
   ```
2. Set your OpenAI API Key in `.env`.

## Running the Application

Start the API server:
```bash
uvicorn app.main:app --reload
```

## Testing

Run the test suite:
## Deployment (Render)

This project includes a `render.yaml` Blueprint for easy deployment.

1.  Push this code to a **GitHub Repository**.
2.  Log in to [Render](https://render.com).
3.  Click **New +** -> **Blueprint**.
4.  Select your repository.
5.  Render will automatically detect the Backend (Docker) and Frontend (Static).
6.  **Important**: You will be prompted to enter your `OPENAI_API_KEY` in the Render dashboard during setup.

The Frontend will automatically be configured to talk to the Backend via the `VITE_API_URL` environment variable.
