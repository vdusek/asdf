from fastapi import FastAPI

from asdf.log_config import logger
from asdf.responses import PrettyJsonResponse

# FastAPI app
app = FastAPI()


@app.get("/")
async def root() -> PrettyJsonResponse:
    logger.debug("Log message from root endpoint")
    content = {"message": "Hello world!"}
    return PrettyJsonResponse(content, indent=2)
