from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os
import re

# Add project root to sys.path to allow importing from src
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

# Import core logic
# Note: On Vercel, we need to ensure dependencies are installed via requirements.txt
try:
    from src.deap.evolution import Evolution
except ImportError:
    # Fallback for when running in an environment where src is not easily resolved
    # or dependencies are missing during build analysis
    Evolution = None

app = FastAPI(docs_url="/api/docs", openapi_url="/api/openapi.json")

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = os.path.join(os.path.dirname(__file__), '../data')

def get_latest_generation():
    max_g = -1
    if not os.path.exists(DATA_DIR):
        return max_g
    for name in os.listdir(DATA_DIR):
        if re.match(r'^g\d+$', name):
            g_num = int(name[1:])
            if g_num > max_g:
                max_g = g_num
    return max_g

@app.get("/")
def read_root_index():
    return {
        "message": "Welcome to MindMutant API",
        "status": "running",
        "documentation": "/api/docs"
    }

@app.get("/api")
def read_root():
    return {
        "message": "MindMutant API is running",
        "endpoints": [
            "/api/status",
            "/api/evolve",
            "/api/docs"
        ]
    }

@app.get("/api/status")
def get_status():
    g = get_latest_generation()
    return {
        "latest_generation": g,
        "data_dir_exists": os.path.exists(DATA_DIR),
        "generations": [d for d in os.listdir(DATA_DIR) if re.match(r'^g\d+$', d)] if os.path.exists(DATA_DIR) else []
    }

@app.post("/api/evolve")
def trigger_evolution(force_disaster: bool = False):
    if Evolution is None:
        return {"status": "error", "message": "Evolution module could not be imported."}
    
    try:
        current_g = get_latest_generation()
        # Initialize Evolution engine
        engine = Evolution()
        
        # Note: On Vercel (Serverless), the file system is ephemeral.
        # Files written to 'data/' will not persist after the function finishes execution.
        # This endpoint is useful for demonstration or if connected to external storage.
        new_g = engine.evolve(current_g, force_disaster=force_disaster)
        
        return {
            "status": "success", 
            "previous_generation": current_g,
            "new_generation": new_g,
            "note": "On serverless environments, generated data is ephemeral."
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# For Vercel, we just need to expose 'app'
