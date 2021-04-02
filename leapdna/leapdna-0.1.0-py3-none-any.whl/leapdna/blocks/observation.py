from leapdna.blocks.locus import Locus
from typing import Optional, Union
from .base import Base
from .allele import Allele


class Observation(Base):
    block_type = 'observation'
    allele: Union[Allele, str]
    count: Optional[int]
    frequency: Optional[float]

    def __init__(self,
                 allele: Union[Allele, str],
                 count: Optional[int] = None,
                 frequency: Optional[float] = None,
                 *args,
                 **kwargs):
        super().__init__(block_type=self.block_type, *args,
                         **kwargs)  # type: ignore
        self.allele = allele
        self.count = count
        self.frequency = frequency

    @property
    def locus(self) -> Union[Locus, str]:
        return self.allele.locus

    def resolve_deps_from_blob(self, blob):
        if isinstance(self.allele, str) and self.allele in blob:
            self.allele = blob[self.allele]