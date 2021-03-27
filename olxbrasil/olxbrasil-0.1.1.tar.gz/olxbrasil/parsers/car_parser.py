from olxbrasil.parsers.item_parser import ItemParser


class CarParser(ItemParser):
    def is_flex(self) -> bool:
        return self.properties["fuel"].lower().strip() == "flex"

    def is_exchangeable(self) -> str:
        return self.properties["exchange"].lower().strip() == "sim"

    def is_sole_owner(self):
        return self.properties["owner"].lower().strip() == "sim"

    def is_tax_paid(self):
        return self.properties["financial"].lower().strip() == "ipva pago"
