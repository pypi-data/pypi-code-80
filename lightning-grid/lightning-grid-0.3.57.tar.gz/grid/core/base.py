from grid.client import Grid


class GridObject:
    """
    Base object. Inherited by all user-facing object; providing
    common methods and the Grid client instance.
    """
    def __init__(self):
        self.client = Grid()

    def _update_meta(self) -> None:
        """Updates object attributes with metadata from backend."""
        if not self._data:
            return

        for k, v in self._data.items():
            setattr(self, k, v)

    def refresh(self):  # pragma: no cover
        """
        Refreshes object metadata. This makes a query to Grid to fetch the
        object's latest data.
        """
        raise NotImplementedError
