from typing import Union

from leapdna.blocks.base import Base
from leapdna.blocks.locus import Locus


class Allele(Base):
    block_type: str = 'allele'
    name: str
    locus: Union[Locus, str]

    def __init__(self, name: str, locus: Union[Locus, str], *args, **kwargs):
        super().__init__(block_type=self.block_type, *args,
                         **kwargs)  # type: ignore

        self.name = name
        self.locus = locus

    def resolve_deps_from_blob(self, blob):
        if isinstance(self.locus, str) and self.locus in blob:
            locus = blob[self.locus]
            if locus.block_type == 'locus':
                self.locus = blob[self.locus]

    def __str__(self):
        return f'<{self.block_type.capitalize()}: {self.name}@{self.locus}>'
