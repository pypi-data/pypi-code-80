class HowLongToBeatTime:
    def __init__(self, name: str, content: str, accuracy: int):
        self.name = name
        self.original_content = content
        value, unit = self.content_to_value_unit(content)
        self.value = value
        self.unit = unit
        self.accuracy = accuracy

    @staticmethod
    def content_to_value_unit(content: str):
        value, unit = content.split(" ") if content != "--" else (None, None)
        if value.endswith("½"):
            num_value = int(value[:-1]) + 0.5
        else:
            num_value = int(value)
        return num_value, unit.lower()

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"name={repr(self.name)}, "
            f"value={repr(self.value)}, unit={repr(self.unit)}, "
            f"accuracy={repr(self.accuracy)})"
        )

    def __str__(self):
        time_str = f"{self.value} {self.unit}" if self.value else "N/A"
        return f"{self.name}: {time_str}"


class HowLongToBeatGame:
    def __init__(self, raw_game: dict):
        self.name = raw_game.get("name")
        self.id = raw_game.get("id")
        self.times = {}
        for time_type, time_details in raw_game["times"].items():
            self.times[time_type] = HowLongToBeatTime(
                name=time_type,
                content=time_details.get("content"),
                accuracy=time_details.get("accuracy"),
            )

    def get_time(self, type_="Main Story"):
        return self.times.get(type_)

    @property
    def main_story(self):
        return self.get_time("Main Story")

    @property
    def main_extra(self):
        return self.get_time("Main + Extra")

    @property
    def completionist(self):
        return self.get_time("Completionist")

    def __repr__(self):
        return f"{self.__class__.__name__}(name={repr(self.name)}, id={repr(self.id)})"

    def __str__(self):
        times_str = "\n".join(f"- {time}" for time in self.times)
        return f"{self.name} (id: {self.id})\n" + times_str
