from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from src.core.settings import application_settings

security = HTTPBearer(auto_error=False)


async def token_access(credentials: HTTPAuthorizationCredentials = Depends(security)) -> None:
    if credentials is None or application_settings.APP_AUTH_TOKEN != credentials.credentials:
        raise HTTPException(status_code=401, detail="Invalid authorization code!")
