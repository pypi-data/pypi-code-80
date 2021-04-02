from leapdna.blocks.locus import Locus
from leapdna.errors import LeapdnaError
from leapdna import blocks
from leapdna.blocks.base import Base
from .support import TestCase

from leapdna.blob import LeapdnaBlob


class TestFromdict(TestCase):
    def test_can_be_instantiated(self):
        blob = LeapdnaBlob()
        self.assertTrue(blob is not None)

    def test_refuses_non_leapdna_data(self):
        data = {'bogus': 1}
        with self.assertRaises(LeapdnaError):
            LeapdnaBlob(data)

        data = {'leapdna': {'block_type': 'locus'}, 'name': 'l1'}
        with self.assertRaises(LeapdnaError):
            LeapdnaBlob(data)

    def test_parse_block(self):
        data = {'leapdna': {'block_type': 'locus'}, 'name': 'l1'}
        locus = LeapdnaBlob.parse_block(data)
        self.assertTrue(isinstance(locus, Locus))
        self.assertTrue(locus.name, 'l1')

    def test_parse_block_fails_for_non_leapdna_data(self):
        data = {'bogus': 1}
        with self.assertRaises(LeapdnaError):
            LeapdnaBlob.parse_block(data)

        data = {'leapdna': {'incomplete': True}}
        with self.assertRaises(LeapdnaError):
            LeapdnaBlob.parse_block(data)

        data = {'leapdna': {'block_type': 'bogus'}, 'name': 'l1'}
        with self.assertRaises(LeapdnaError):
            LeapdnaBlob.parse_block(data)

    def test_generates_ids_for_blocks_without_id(self):
        block = Base()
        self.assertTrue(block.id is None)

        blob = LeapdnaBlob()
        initial_counter = blob.id_counter
        gen_id = blob.generate_id(block)

        self.assertEqual(gen_id, block.id)
        self.assertEqual(blob.id_counter, initial_counter + 1)

    def test_generates_ids_for_blocks_with_id(self):
        block = Base(id='my_id')
        self.assertTrue(block.id is not None)

        blob = LeapdnaBlob()
        initial_counter = blob.id_counter
        gen_id = blob.generate_id(block)
        self.assertEqual(gen_id, block.id)
        self.assertEqual(blob.id_counter, initial_counter)