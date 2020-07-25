import uvicorn
from fastapi import FastAPI, Depends

from endpoints.iam_endpoints import router as iam_router, user_is_authenticated
from endpoints.initiative_endpoins import router as initiative_router
from endpoints.workspace_endpoints import router as workspace_router

app = FastAPI()
app.include_router(iam_router, tags=["IAM"])
app.include_router(initiative_router, tags=["Initiative"], dependencies=[Depends(user_is_authenticated)])
app.include_router(workspace_router, tags=["Workspace"], dependencies=[Depends(user_is_authenticated)])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
