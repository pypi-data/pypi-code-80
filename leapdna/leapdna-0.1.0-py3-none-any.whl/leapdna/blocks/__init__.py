from .base import Base
from .allele import Allele
from .locus import Locus
from .observation import Observation

BLOCKTYPE_MAP = {
    Base.block_type: Base,
    Allele.block_type: Allele,
    Locus.block_type: Locus,
    Observation.block_type: Observation
}