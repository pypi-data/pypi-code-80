class SuccessRespData:
    """[data]"""

    def __init__(self, json: dict) -> None:
        self.file = SuccessRespDataFile(json.get("file"))


class SuccessRespDataFile:
    """[data][file]"""

    def __init__(self, json: dict) -> None:
        self.url = SuccessRespDataFileUrl(json.get("url"))
        self.metadata = SuccessRespDataFileMetadata(json.get("metadata"))


class SuccessRespDataFileUrl:
    """[data][file][url]"""

    def __init__(self, json: dict) -> None:
        self.full = json.get("full")
        self.short = json.get("short")


class SuccessRespDataFileMetadata:
    """[data][file][metadata]"""

    def __init__(self, json: dict) -> None:
        self.id = json.get("id")
        self.name = json.get("name")
        self.size = SuccessRespDataFileMetadataSize(json.get("size"))


class SuccessRespDataFileMetadataSize:
    """[data][file][metadata][size]"""

    def __init__(self, json: dict) -> None:
        self.bytes = json.get("bytes")
        self.readable = json.get("readable")


class ErrorResp:
    """[error]"""

    def __init__(self, json: dict) -> None:
        self.message = json.get("message")
        self.type = json.get("type")
        self.code = json.get("code")