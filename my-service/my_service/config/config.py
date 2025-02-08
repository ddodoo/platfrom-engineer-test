from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
from pydantic import AnyHttpUrl


class Settings(BaseSettings):
    BACKEND_ORIGINS: List[AnyHttpUrl] = []
    FASTAPI_PROJECT_NAME: str = "my-service"
    LOG_LEVEL: str = "DEBUG"

    # ArgoCD Config defaults
    ARGOCD_SERVER: str = "https://localhost" 
    ARGOCD_PASSWORD: str = "daniel.dodoo"
    ARGOCD_USERNAME: str = "ops"                            
    TOKEN_CACHE_TTL: int = 600
    
    ARGOCD_TOKEN: str =  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhcmdvY2QiLCJzdWIiOiJvcHM6YXBpS2V5IiwibmJmIjoxNzM4OTcxODM1LCJpYXQiOjE3Mzg5NzE4MzUsImp0aSI6IjRmZTYxNGVhLTgyZmItNDJkMi1hZWEwLTczOGI2ZTUzZGIxMCJ9.sHaeMSv688vhCUgeDb0Lnf6qlfEkNxL6a-HEgUR8miU"

    model_config = SettingsConfigDict(env_nested_delimiter='__')


settings = Settings(_env_file=".env")
