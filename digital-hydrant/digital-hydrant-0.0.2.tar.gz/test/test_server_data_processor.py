import os
import sqlite3
import unittest
from unittest.mock import patch

from digital_hydrant.server_data_processor import Processor


class TestServerDataProcessor(unittest.TestCase):
    def setUp(self):
        self.database_file = "test.sqlite"
        self.processor = Processor(self.database_file)

        self.cursor = sqlite3.connect(self.database_file).cursor()

    def tearDown(self):
        if os.path.exists(self.database_file):
            os.remove(self.database_file)

    def test_init(self):
        self.cursor.execute(
            """ SELECT count(name) FROM sqlite_master WHERE type='table' AND name='unique_ips' """
        )

        self.assertEqual(1, self.cursor.fetchone()[0])

    @patch("digital_hydrant.server_data_processor.Processor.process_ips")
    def test_process_data(self, mock):
        ips = [1, 2, 3, 4]
        self.processor.process_server_data({"ips": ips})

        mock.assert_called_once_with(ips)

    def test_process_ips(self):
        self.processor.process_ips([0, 1, 2, 3, 4, 3])

        self.cursor.execute("SELECT id, ip FROM unique_ips ORDER BY ip ASC")

        ips = self.cursor.fetchall()

        self.assertEqual(5, len(ips))

        for i in range(5):
            self.assertEqual(str(i), ips[i][1])

    def test_process_ips_duplicates(self):
        self.processor.process_ips([0, 1, 2, 3, 4, 3])

        self.cursor.execute("SELECT id, ip FROM unique_ips ORDER BY ip ASC")

        ips = self.cursor.fetchall()

        self.assertEqual(5, len(ips))

        for i in range(5):
            self.assertEqual(str(i), ips[i][1])

        self.processor.process_ips([3, 4, 5, 6])

        self.cursor.execute("SELECT id, ip FROM unique_ips ORDER BY ip ASC")

        ips = self.cursor.fetchall()

        self.assertEqual(7, len(ips))

        for i in range(7):
            self.assertEqual(str(i), ips[i][1])
