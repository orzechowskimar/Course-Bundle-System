# Course-Bundle-System

This is a FastAPI application that generates resource bundle quotes based on teacher requests and resource provider data. The application processes a teacher's request for educational resources and calculates quotes for each provider based on the topics they offer and the requested content level.


## API Endpoints

### POST `/calculate_quotes/`

**Description:** Calculates quotes for providers based on the topics requested and provider configurations.

---

## Running the Application

1. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**

   ```bash
    uvicorn main:app --host 0.0.0.0 --port 8080 --reload
   ```


## Testing

1. **Install Test Dependencies**

   ```bash
   pip install pytest
   ```

2. **Run Tests**

   ```bash
   pytest test.py
   ```

---
