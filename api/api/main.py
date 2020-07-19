import uvicorn
from fastapi import FastAPI, Depends

from endpoints.iam_endpoints import router as iam_router, get_current_user
from endpoints.initiative_endpoins import router as initiative_router

app = FastAPI()
app.include_router(initiative_router, tags=["Initiative"], dependencies=[Depends(get_current_user)])
app.include_router(iam_router, tags=["IAM"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
