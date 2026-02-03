from fastapi import FastAPI

app = FastAPI(title="Agentic Healthcare")

@app.get("/")
def health_check():
    return {"status": "running"}
