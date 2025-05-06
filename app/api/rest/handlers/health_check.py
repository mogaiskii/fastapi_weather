from starlette.responses import JSONResponse

from api.rest import rest_app
from settings import settings


@rest_app.get("/health")
async def health_check():
    content = {"status": "OK", "version": settings.version}
    headers = {"Cache-control": "max-age: 200, must-revalidate"}
    return JSONResponse(content=content, headers=headers)
