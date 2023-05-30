from xml.etree import ElementTree as ET

from asdf.log_config import logger


class XmlReader:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def get_num_of_items(self) -> int:
        tree = ET.parse(self.file_path)
        root = tree.getroot()
        cnt = 0

        # In case there would be more "items" nodes
        for root_items in root.findall("items"):
            logger.debug("type(root_items): %s", type(root_items))

            if isinstance(root_items, ET.Element):
                cnt += len(root_items.findall("item"))

        return cnt

    def get_item_names(self) -> list[str]:
        result: list[str] = []

        with open(self.file_path, "rb") as file:
            for _, element in ET.iterparse(file, events=("start",)):
                if element.tag == "item":
                    name = element.attrib.get("name")

                    if name is not None:
                        result.append(name)
                    element.clear()

        return result

    def get_spare_parts(self) -> dict[str, list[str]]:
        """
        items -> item -> parts -> part -> item
        """
        tree = ET.parse(self.file_path)
        root = tree.getroot()
        result: dict[str, list[str]] = {}

        for root_items in root.findall("items"):
            for root_items_item in root_items.findall("item"):
                item_name = root_items_item.attrib.get("name")

                if item_name is None:
                    continue

                for parts in root_items_item.findall("parts"):
                    for part in parts.findall("part"):
                        if part.attrib.get("name") != "Náhradní díly":
                            continue

                        for item in part.findall("item"):
                            spare_part_name = item.attrib.get("name")

                            if spare_part_name is None:
                                continue

                            try:
                                result[item_name].append(spare_part_name)
                            except KeyError:
                                result[item_name] = [spare_part_name]

        return result
