from fastapi import Depends, FastAPI
from src.api.router import router
from src.core.authentication import token_access
from src.core.settings import application_settings
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

# Application Base
app = FastAPI(
    title=application_settings.APP_TITLE,
    description="...",
)
app.include_router(router, dependencies=[Depends(token_access)])

app.add_middleware(ProxyHeadersMiddleware, trusted_hosts='*')


if application_settings.APP_DEBUG:
    from pyngrok import ngrok

    http_tunnel = ngrok.connect(8000)
    print('ngrok tunnel "{}" -> "http://0.0.0.0:{}"'.format(http_tunnel.public_url, 8000))
