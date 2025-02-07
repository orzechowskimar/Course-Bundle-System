import json
import os
from fastapi import FastAPI, HTTPException

from execptions import ProviderDataError, QuoteCalculationError
from schemas import RequestModel
from service import QuoteCalculator
from logger import logger

app = FastAPI()

# Load providers from external configuration file
PROVIDERS_FILE = "providers.json"

def load_providers():
    if not os.path.exists(PROVIDERS_FILE):
        logger.error(f"{PROVIDERS_FILE} not found.")
        raise HTTPException(status_code=404, detail=f"{PROVIDERS_FILE} not found.")
    try:
        with open(PROVIDERS_FILE, "r") as file:
            provider_data = json.load(file)
            logger.info("Successfully loaded provider data.")
            return provider_data
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing JSON in {PROVIDERS_FILE}: {e}")
        raise HTTPException(status_code=500, detail="Error parsing provider data.")
    except Exception as e:
        logger.error(f"Unexpected error while loading providers: {e}")
        raise HTTPException(status_code=500, detail="Error loading provider data.")

@app.post("/calculate_quotes/")
def calculate_quotes(request: RequestModel):
    try:
        provider_data = load_providers()
        calculator = QuoteCalculator(request.model_dump(), provider_data)
        quotes = calculator.calculate_quotes()
        return {"quotes": quotes}
    except ProviderDataError as e:
        logger.exception("Invalid provider data format.")
        raise HTTPException(status_code=500, detail=str(e))
    except QuoteCalculationError as e:
        logger.exception("Error during quote calculation.")
        raise HTTPException(status_code=400, detail=str(e))
    except KeyError as e:
        logger.error(f"Missing key in data: {e}")
        raise HTTPException(status_code=400, detail=f"Missing key: {e}")
    except ValueError as e:
        logger.error(f"Value error during calculation: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid data: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")
