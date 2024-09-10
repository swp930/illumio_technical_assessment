import unittest
import os
import shutil
import csv

# Import the functions from main.py
from main import delete_file, get_lookup_table, get_protocol_num_to_str, process_flow_logs, write_tag_counts_to_output, write_port_combination_frequency

class TestFileProcessing(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up class-level variables for pre-filled input files
        cls.test_dir = 'tests'
        cls.lookup_file = os.path.join(cls.test_dir, 'lookup.csv')
        cls.protocol_file = os.path.join(cls.test_dir, 'protocol-numbers.csv')
        cls.flow_log_file = os.path.join(cls.test_dir, 'sample_flow_logs.txt')
        cls.tag_counts_file = os.path.join(cls.test_dir, 'tag_counts.csv')
        cls.port_protocol_counts_file = os.path.join(cls.test_dir, 'port_protocol_counts.csv')

        # Ensure the output files are not present before running the tests
        if os.path.isfile(cls.tag_counts_file):
            os.remove(cls.tag_counts_file)
        if os.path.isfile(cls.port_protocol_counts_file):
            os.remove(cls.port_protocol_counts_file)

    @classmethod
    def tearDownClass(cls):
        # Clean up output files after tests
        if os.path.isfile(cls.tag_counts_file):
            os.remove(cls.tag_counts_file)
        if os.path.isfile(cls.port_protocol_counts_file):
            os.remove(cls.port_protocol_counts_file)

    def test_process_flow_logs(self):
        lookup_table = get_lookup_table(self.lookup_file)
        protocol_num_to_str = get_protocol_num_to_str(self.protocol_file)
        tag_frequency, port_combination_frequency = process_flow_logs(self.flow_log_file, lookup_table, protocol_num_to_str)
        expected_tag_frequency = {'Untagged': 8, 'sv_P2': 1, 'sv_P1': 2, 'email': 3}
        expected_port_combination_frequency = {'49153': {'tcp': 1}, '49154': {'tcp': 1}, '49155': {'tcp': 1}, '49156': {'tcp': 1}, '49157': {'tcp': 1}, '49158': {'tcp': 1}, '80': {'tcp': 1}, '1024': {'tcp': 1}, '443': {'tcp': 1}, '23': {'tcp': 1}, '25': {'tcp': 1}, '110': {'tcp': 1}, '993': {'tcp': 1}, '143': {'tcp': 1}}
        self.assertEqual(tag_frequency, expected_tag_frequency)
        self.assertEqual(port_combination_frequency, expected_port_combination_frequency)

if __name__ == '__main__':
    unittest.main()
