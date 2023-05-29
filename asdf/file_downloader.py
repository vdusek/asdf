from __future__ import annotations

import asyncio
import os
import shutil
import zipfile
from types import TracebackType
from typing import Type

import httpx

from asdf.log_config import logger


class FileDownloader:
    def __init__(self, url: str, unzip: bool = True) -> None:
        self.url = url
        self.file_path: None | str = None
        self.unzip_dir: None | str = None
        self.unzip = unzip

    @property
    def unzip_file_path(self) -> str | None:
        filenames = os.listdir(self.unzip_dir)
        if self.unzip_dir:
            return os.path.join(self.unzip_dir, filenames[0])
        logger.error("self.unzipdir is None")
        return None

    async def __aenter__(self) -> FileDownloader:
        logger.debug("Entering FileDownloader...")
        self.file_path = await self._download_file(self.url)
        if self.unzip:
            self.unzip_dir = await asyncio.to_thread(self._unzip_file, self.file_path)
        return self

    async def __aexit__(
        self,
        exc_type: Type[BaseException],
        exc_value: BaseException,
        traceback: TracebackType,
    ) -> None:
        logger.debug("Exiting FileDownloader...")
        if self.file_path is not None:
            await self._delete_file(self.file_path)
        if self.unzip_dir is not None:
            await self._delete_dir(self.unzip_dir)

    @staticmethod
    async def _download_file(url: str) -> str:
        logger.debug("Downloading file: %s", url)
        file_name = url.split("/")[-1]
        file_path = os.path.join("/tmp", file_name)

        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            with open(file_path, "wb") as file:
                async for chunk in response.aiter_bytes():
                    file.write(chunk)

        logger.info("File %s was downloaded and stored to %s", url, file_path)
        return file_path

    @staticmethod
    def _unzip_file(file_path: str) -> str | None:
        logger.debug("Unzipping file: %s", file_path)
        try:
            unzip_dir = os.path.join("/tmp", "unzipped")
            os.makedirs(unzip_dir, exist_ok=True)
            with zipfile.ZipFile(file_path, "r") as zip_ref:
                zip_ref.extractall(unzip_dir)
            logger.info("File %s was unzipped and stored at: %s", file_path, unzip_dir)
            return unzip_dir
        except zipfile.BadZipFile:
            logger.error("Invalid ZIP file: %s", file_path)
            return None

    @staticmethod
    async def _delete_file(file_path: str) -> None:
        logger.debug("Deleting file on: %s", file_path)
        try:
            await asyncio.to_thread(os.remove, file_path)
            logger.info("Deleted file: %s", file_path)
        except FileNotFoundError:
            logger.error("File not found: %s", file_path)
        except IsADirectoryError:
            logger.error("Cannot delete directory: %s", file_path)

    @staticmethod
    async def _delete_dir(dir_path: str) -> None:
        logger.debug("Deleting dir on: %s", dir_path)
        await asyncio.to_thread(shutil.rmtree, dir_path, ignore_errors=True)
        logger.info("Deleted dir: %s", dir_path)
