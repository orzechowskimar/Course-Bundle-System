from fastapi import FastAPI, HTTPException
from schemas import RequestModel
from service import QuoteCalculator
import json
import os

app = FastAPI()

# Load providers from external configuration file
PROVIDERS_FILE = "providers.json"

def load_providers():
    if not os.path.exists(PROVIDERS_FILE):
        raise FileNotFoundError(f"{PROVIDERS_FILE} not found.")
    with open(PROVIDERS_FILE, "r") as file:
        return json.load(file)

@app.post("/calculate_quotes/")
def calculate_quotes(request: RequestModel):
    try:
        provider_data = load_providers()  # Load provider topics dynamically
        calculator = QuoteCalculator(request.dict(), provider_data)
        quotes = calculator.calculate_quotes()
        return {"quotes": quotes}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
