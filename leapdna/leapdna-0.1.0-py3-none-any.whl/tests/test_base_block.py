import leapdna
from .support import TestCase

from leapdna.blocks import Base


class TestBaseBlock(TestCase):
    def test_can_be_instantiated_from_a_dict(self):
        data = {
            'leapdna': {
                'block_type': 'base',
                'id': 1234
            },
            'user': {
                'custom_prop': 123
            }
        }

        res = Base(**data)
        self.assertEqual(res.block_type, 'base')
        self.assertEqual(res.id, 1234)
        self.assertEqual(res.user['custom_prop'], 123)

    def test_direct_arguments_take_precedence_over_leapdna(self):
        block = Base(id='1',
                     block_type='allele',
                     leapdna={
                         'id': 'something else',
                         'block_type': 'something else'
                     })
        self.assertEqual(block.id, '1')
        self.assertEqual(block.block_type, 'allele')

    def test_can_be_converted_to_dict(self):
        data = {
            'leapdna': {
                'block_type': 'base',
                'id': '1234'
            },
            'user': {
                'custom_prop': 123
            }
        }
        block = Base(**data)
        self.assertEqual(data, block.asdict())

    def test_has_string_representation(self):
        block = Base(id='123')
        self.assertIn('123', str(block))
        self.assertIn('123', repr(block))