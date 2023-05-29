import os

from fastapi import FastAPI

from asdf.consts import SRC_FILE_URL
from asdf.file_downloader import FileDownloader
from asdf.log_config import logger
from asdf.responses import PrettyJsonResponse

# FastAPI app
app = FastAPI()


@app.get("/")
async def root() -> PrettyJsonResponse:
    logger.debug("Log message from root endpoint")
    content = {"message": "Hello world!"}
    return PrettyJsonResponse(content, indent=2)


@app.get("/1/")
async def one() -> PrettyJsonResponse:
    logger.debug("Log message from one endpoint")

    async with FileDownloader(SRC_FILE_URL) as fd:
        file_path = fd.file_path
        logger.debug("file_path: %s", fd.file_path)
        logger.debug("unzip_file_path: %s", fd.unzip_file_path)

    logger.debug("listdir /tmp: %s", os.listdir("/tmp"))
    return PrettyJsonResponse({"file_path": file_path}, indent=2)
