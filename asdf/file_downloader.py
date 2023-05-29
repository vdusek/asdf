from __future__ import annotations

import asyncio
import os
from types import TracebackType
from typing import Type

import httpx

from asdf.log_config import logger


async def _download_file(url: str) -> str:
    logger.debug("Downloading file on: %s", url)
    file_name = url.split("/")[-1]
    file_path = os.path.join("/tmp", file_name)

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        with open(file_path, "wb") as file:
            async for chunk in response.aiter_bytes():
                file.write(chunk)

    logger.info("File %s was downloaded and stored to: %s", url, file_path)
    return file_path


async def _delete_file(file_path: str) -> None:
    logger.debug("Deleting file on: %s", file_path)
    try:
        await asyncio.to_thread(os.remove, file_path)
        logger.info("Deleted file: %s", file_path)
    except FileNotFoundError:
        logger.error("File not found: %s", file_path)
    except IsADirectoryError:
        logger.error("Cannot delete directory: %s", file_path)


class FileDownloader:
    def __init__(self, url: str) -> None:
        self.url = url
        self.file_path: None | str = None

    async def __aenter__(self) -> FileDownloader:
        logger.debug("Entering FileDownloader...")
        self.file_path = await _download_file(self.url)
        return self

    async def __aexit__(
        self,
        exc_type: Type[BaseException],
        exc_value: BaseException,
        traceback: TracebackType,
    ) -> None:
        logger.debug("Exiting FileDownloader...")
        if self.file_path is not None:
            await _delete_file(self.file_path)