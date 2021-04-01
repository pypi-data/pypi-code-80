from pathlib import Path


class PandoraModel:
    """PandoraModel contains information about a machine learning model."""

    language: str
    name: str
    version: str
    unzip: bool
    filename: str
    path: Path

    def __init__(
        self,
        language: str,
        name: str,
        version: str,
        unzip: bool,
        filename: str,
        path: Path = None
    ):
        self.language = language
        self.name = name
        self.version = version
        self.unzip = unzip
        self.filename = filename
        self.path = path

    def __eq__(self, other):
        return (
            self.language == other.language
            and self.name == other.name
            and self.version == other.version
            and self.unzip == other.unzip
            and self.filename == other.filename
        )

    def __ne__(self, other):
        return (
            self.language != other.language
            or self.name != other.name
            or self.version != other.version
            or self.unzip != other.unzip
            or self.filename != other.filename
        )
