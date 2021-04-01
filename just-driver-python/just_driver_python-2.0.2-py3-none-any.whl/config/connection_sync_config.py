class ConnectionSyncConfig:
    def __init__(self, catalog: str = "default", dirty: bool = True):
        self._catalog = catalog
        self._dirty = dirty

    @property
    def catalog(self):
        return self._catalog

    def __str__(self):
        return {"catalog": self._catalog, "dirty": self._dirty}.__str__()
