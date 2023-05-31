from time import time
from xml.etree import ElementTree as ET

from asdf.log_config import logger


class XmlReader:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def get_num_of_items(self) -> int:
        """
        export_full -> items -> item -> ...
        """
        start_time = time()
        context = ET.iterparse(self.file_path, events=("start", "end"))
        _, root = next(context)
        DESIDER_DEPTH = 2

        cnt = 0
        depth = 0
        for event, element in context:
            if event == "start":
                depth += 1
                if element.tag == "item" and depth == DESIDER_DEPTH:
                    cnt += 1

            if event == "end":
                depth -= 1
                element.clear()

                if element.tag == "items":
                    root.clear()
                    break

            root.clear()

        end_time = time()
        elapsed_time = end_time - start_time
        logger.info("[1] Processing time: %s seconds", elapsed_time)

        return cnt

    def get_item_names(self) -> list[str]:
        """
        export_full -> items -> item -> ...
        """
        start_time = time()
        context = ET.iterparse(self.file_path, events=("start", "end"))
        _, root = next(context)
        DESIDER_DEPTH = 2

        result: list[str] = []
        depth = 0
        for event, element in context:
            if event == "start":
                depth += 1
                if element.tag == "item" and depth == DESIDER_DEPTH:
                    name = element.attrib.get("name")
                    result.append(name)

            if event == "end":
                depth -= 1
                element.clear()

                if element.tag == "items":
                    root.clear()
                    break

            root.clear()

        end_time = time()
        elapsed_time = end_time - start_time
        logger.info("[2] Processing time: %s seconds", elapsed_time)

        return result

    def get_spare_parts(self) -> list[str]:
        """
        export_full -> items -> item -> parts -> part -> item
        """
        start_time = time()
        context = ET.iterparse(self.file_path, events=("start", "end"))
        _, root = next(context)
        DESIDER_DEPTH = 5

        result: list[str] = []
        depth = 0
        for event, element in context:
            if event == "start":
                depth += 1
                if element.tag == "item" and depth == DESIDER_DEPTH:
                    spare_part_name = element.attrib.get("name")
                    result.append(spare_part_name)

            if event == "end":
                depth -= 1
                element.clear()

                if element.tag == "items":
                    root.clear()
                    break

            root.clear()

        end_time = time()
        elapsed_time = end_time - start_time
        logger.info("[3] Processing time: %s seconds", elapsed_time)

        return result
