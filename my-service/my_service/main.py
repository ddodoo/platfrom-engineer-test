import uvicorn
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
import httpx

from my_service.config.config import settings
from my_service.models.models import HealthCheckResponse
from my_service.utils.logger import setup_logger
from my_service.api.v1 import api

logger = setup_logger()
logger.debug(f"Running with config: {settings}")

# Load ArgoCD server and token securely from settings
ARGOCD_SERVER = settings.ARGOCD_SERVER  
ARGOCD_TOKEN = settings.ARGOCD_TOKEN  

def get_application():
    _app = FastAPI(title=settings.FASTAPI_PROJECT_NAME)  
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
    return _app

app = get_application()
app.include_router(api.router)

@app.get("/healthcheck")
async def healthcheck() -> HealthCheckResponse:
    logger.debug("healthcheck hit")
    return HealthCheckResponse(
        status_code=status.HTTP_200_OK,
        message="Server is running!"
    )

async def get_argocd_data(endpoint: str):
    headers = {"Authorization": f"Bearer {ARGOCD_TOKEN}"}
    async with httpx.AsyncClient(verify=False) as client:
        try:
            response = await client.get(f"{ARGOCD_SERVER}{endpoint}", headers=headers)
            logger.debug(f"ArgoCD API Response [{response.status_code}] for {endpoint}: {response.text}")  
            response.raise_for_status()
            json_data = response.json()
            logger.debug(f"Parsed JSON: {json_data}")  
            return json_data
        except httpx.HTTPStatusError as http_err:
            logger.error(f"HTTP error [{http_err.response.status_code}] for {ARGOCD_SERVER}{endpoint}: {http_err.response.text}")
        except httpx.RequestError as req_err:
            logger.error(f"Request error while calling {ARGOCD_SERVER}{endpoint}: {str(req_err)}")
        except Exception as e:
            logger.error(f"Unexpected error while calling {ARGOCD_SERVER}{endpoint}: {str(e)}")
        finally:
            await client.aclose()  # Ensure connection is closed properly
        return {}  # Return an empty dictionary instead of None


@app.get("/api/v1/argocd/application_status")
async def get_application_status():
    data = await get_argocd_data("/api/v1/applications") or {}
    items = data.get("items")

    if items is None:  # Handle `items: null` case
        logger.warning(f"ArgoCD returned null for applications: {data}")
        return {"applications": []}  # Return an empty list instead of an error

    applications = [
        {
            "application_name": app.get("metadata", {}).get("name", "Unknown"),
            "status": app.get("status", {}).get("sync", {}).get("status", "Unknown"),
        }
        for app in items
    ]
    return {"applications": applications}


@app.get("/api/v1/argocd/list_projects")
async def get_projects():
    data = await get_argocd_data("/api/v1/projects") or {}
    items = data.get("items")

    if items is None:  # Handle `items: null` case
        logger.warning(f"ArgoCD returned null for projects: {data}")
        return {"projects": []}  # Return an empty list instead of an error

    projects = [
        {
            "project_name": proj.get("metadata", {}).get("name", "Unknown"),
            "namespace": "argocd",
        }
        for proj in items
    ]
    return {"projects": projects}


if __name__ == "__main__":
    uvicorn.run("my_service.main:app", port=9000)
