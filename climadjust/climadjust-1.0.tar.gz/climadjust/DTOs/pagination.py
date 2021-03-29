from enum import Enum


class SortDirectionEnum(Enum):
    ASC = "ASC"
    DESC = "DESC"


class PaginationDTO:
    def __init__(self, page: int, size: int, sort_field: str,
                 sort_direction: str):
        """
        @param page: number of page
        @param size: size of page
        @param sort: field,ASC|DESC
        """
        self.page = page
        self.size = size
        try:
            sort_direction = SortDirectionEnum(sort_direction).value if sort_direction is not None else None
        except ValueError:
            raise Exception("Invalid sort direction. Valid directions are ASC and DESC")

        if sort_field is not None:
            self.sort = sort_field + "," + sort_direction

    def get_dict(self):
        d = self.__dict__.copy()
        for key, value in self.__dict__.items():
            if value is None:
                d.pop(key)
        return d