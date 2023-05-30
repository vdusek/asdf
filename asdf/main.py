import asyncio

from fastapi import FastAPI

from asdf.consts import SRC_FILE_URL
from asdf.file_downloader import FileDownloader
from asdf.log_config import logger
from asdf.responses import PrettyJsonResponse
from asdf.xml_reader import XmlReader

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
        logger.debug("file_path: %s", fd.file_path)
        logger.debug("unzip_file_path: %s", fd.unzip_file_path)

        xml_reader = XmlReader(fd.unzip_file_path)
        num_of_items = await asyncio.to_thread(xml_reader.get_num_of_items)

    return PrettyJsonResponse({"num_of_items": num_of_items}, indent=2)


@app.get("/2/")
async def two() -> PrettyJsonResponse:
    logger.debug("Log message from two endpoint")

    async with FileDownloader(SRC_FILE_URL) as fd:
        logger.debug("file_path: %s", fd.file_path)
        logger.debug("unzip_file_path: %s", fd.unzip_file_path)

        xml_reader = XmlReader(fd.unzip_file_path)
        item_names = await asyncio.to_thread(xml_reader.get_item_names)

    return PrettyJsonResponse({"item_names": item_names}, indent=2)


@app.get("/3/")
async def three() -> PrettyJsonResponse:
    logger.debug("Log message from three endpoint")

    async with FileDownloader(SRC_FILE_URL) as fd:
        logger.debug("file_path: %s", fd.file_path)
        logger.debug("unzip_file_path: %s", fd.unzip_file_path)

        xml_reader = XmlReader(fd.unzip_file_path)
        spare_items = await asyncio.to_thread(xml_reader.get_spare_parts)

    return PrettyJsonResponse({"spare_items": spare_items}, indent=2)
