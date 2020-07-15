import uvicorn
from fastapi import FastAPI
from endpoints.initiative_endpoins import router as initiative_router

app = FastAPI()
app.include_router(initiative_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
