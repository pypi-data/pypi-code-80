__all__ = [
    "attriclass"
]

from typing import Optional

class Attriclass:

    attributes: dict[str, Optional[str]]

    def extract(self) -> dict[str, object]:
        result = dict[str, object]()
        for attr, name in self.attributes.items():
            value = getattr(self, attr)
            if isinstance(value, Attriclass):
                result.update(value.extract())
            elif name and value != None:
                result[name] = value
        return result

def attriclass(**attributes: Optional[str]) -> type[Attriclass]:
    return type("Attriclass", (Attriclass,), {
        "attributes": attributes
    })