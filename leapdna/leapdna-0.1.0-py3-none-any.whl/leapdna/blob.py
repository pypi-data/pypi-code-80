from .blocks import BLOCKTYPE_MAP, Base
from .errors import LeapdnaError


class LeapdnaBlob(dict):
    id_counter: int

    def __init__(self, data=None):
        if data:
            if not ('leapdna' in data):
                raise LeapdnaError('data is not a leapdna object')

            if 'block_type' not in data[
                    'leapdna'] or data['leapdna']['block_type'] != 'blob':
                raise LeapdnaError(
                    'data is not a leapdna blob. Try loading with LeapdnaBlob.parse_block instead.'
                )

            ids = set(data.keys()) - {'leapdna'}
            self.update(
                {id: LeapdnaBlob.parse_block(data[id], id)
                 for id in ids})
            self.resolve_deps()

        self.id_counter = 1

    @staticmethod
    def parse_block(data, id=None) -> Base:
        if not ('leapdna' in data):
            raise LeapdnaError('object is not a leapdna block')

        if not ('block_type' in data['leapdna']):
            raise LeapdnaError('"block_type" not specified in block')

        try:
            block = BLOCKTYPE_MAP[data['leapdna']['block_type']]
            return block(**data, id=id)
        except KeyError:
            raise LeapdnaError(
                f'unkwon block_type "{data["leapdna"]["block_type"]}"')

    def resolve_deps(self):
        for key in self:
            if key == 'leapdna': continue

            self[key].resolve_deps_from_blob(self)

    def generate_id(self, block: Base) -> str:
        if block.id is None or (block.id in self):
            self.id_counter += 1
            id = f'g.{self.id_counter}'
            block.id = f'g.{self.id_counter}'

        return block.id
