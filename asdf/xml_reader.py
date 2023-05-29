from typing import Any, Generator
from xml.etree.ElementTree import Element
import xml.etree.ElementTree as ET

from asdf.log_config import logger


class XmlReaderError(Exception):
    pass


class XmlReader:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def get_num_of_items(self) -> int:
        tree = ET.parse(self.file_path)
        root = tree.getroot()
        items = root.find("items")
        logger.info("type(items): %s", type(items))
        if isinstance(items, Element):
            return len(items.findall("item"))
        raise XmlReaderError("items is not instance of Element")

    def get_item_names(self) -> Generator[Any, Any, None]:
        # tree = ET.parse(self.file_path)
        # root = tree.getroot()
        # items = root.find("items")
        # for item in items.findall("item"):
        #     yield str(item.attrib["name"])

        with open(self.file_path, "rb") as file:
            context = ET.iterparse(file, events=("start",))
            for _, element in context:
                if element.tag == "item":
                    name = element.attrib.get("name")
                    if name is not None:
                        yield name
                    element.clear()
