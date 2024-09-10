import unittest
import os
import tempfile
import shutil
import csv

# Import the functions from main.py
from main import delete_file, get_lookup_table, get_protocol_num_to_str, process_flow_logs, write_tag_counts_to_output, write_port_combination_frequency

class TestFileProcessing(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()
        
        # Paths for temporary files
        self.lookup_file = os.path.join(self.test_dir, 'lookup.csv')
        self.protocol_file = os.path.join(self.test_dir, 'protocol-numbers.csv')
        self.flow_log_file = os.path.join(self.test_dir, 'sample_flow_logs.txt')
        self.tag_counts_file = os.path.join(self.test_dir, 'tag_counts.csv')
        self.port_protocol_counts_file = os.path.join(self.test_dir, 'port_protocol_counts.csv')

        # Create sample data
        self.create_sample_files()

    def tearDown(self):
        # Remove the temporary directory and all its contents
        shutil.rmtree(self.test_dir)

    def create_sample_files(self):
        # Create a sample lookup table
        with open(self.lookup_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['tag1', 'Description1'])
            writer.writerow(['tag2', 'Description2'])

        # Create a sample protocol number to string mapping
        with open(self.protocol_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['1', 'HTTP'])
            writer.writerow(['2', 'HTTPS'])

        # Create a sample flow log
        with open(self.flow_log_file, 'w') as f:
            f.write("tag1 80 1\n")
            f.write("tag1 80 2\n")
            f.write("tag2 443 1\n")

    def test_delete_file(self):
        # Test deleting a file
        delete_file(self.tag_counts_file)  # Ensure file does not exist
        self.assertFalse(os.path.isfile(self.tag_counts_file))
        with open(self.tag_counts_file, 'w') as f:
            f.write('test')
        self.assertTrue(os.path.isfile(self.tag_counts_file))
        delete_file(self.tag_counts_file)
        self.assertFalse(os.path.isfile(self.tag_counts_file))

    def test_get_lookup_table(self):
        lookup_table = get_lookup_table(self.lookup_file)
        expected = {'tag1': 'Description1', 'tag2': 'Description2'}
        self.assertEqual(lookup_table, expected)

    def test_get_protocol_num_to_str(self):
        protocol_num_to_str = get_protocol_num_to_str(self.protocol_file)
        expected = {'1': 'HTTP', '2': 'HTTPS'}
        self.assertEqual(protocol_num_to_str, expected)

    def test_process_flow_logs(self):
        lookup_table = get_lookup_table(self.lookup_file)
        protocol_num_to_str = get_protocol_num_to_str(self.protocol_file)
        tag_frequency, port_combination_frequency = process_flow_logs(self.flow_log_file, lookup_table, protocol_num_to_str)
        expected_tag_frequency = {'tag1': 2, 'tag2': 1}
        expected_port_combination_frequency = {('80', 'HTTP'): 2, ('443', 'HTTPS'): 1}
        self.assertEqual(tag_frequency, expected_tag_frequency)
        self.assertEqual(port_combination_frequency, expected_port_combination_frequency)

    def test_write_tag_counts_to_output(self):
        tag_frequency = {'tag1': 2, 'tag2': 1}
        write_tag_counts_to_output(self.tag_counts_file, tag_frequency)
        with open(self.tag_counts_file, 'r') as f:
            lines = f.readlines()
        expected_lines = ['tag1,2\n', 'tag2,1\n']
        self.assertEqual(lines, expected_lines)

    def test_write_port_combination_frequency(self):
        port_combination_frequency = {('80', 'HTTP'): 2, ('443', 'HTTPS'): 1}
        write_port_combination_frequency(self.port_protocol_counts_file, port_combination_frequency)
        with open(self.port_protocol_counts_file, 'r') as f:
            lines = f.readlines()
        expected_lines = ['80,HTTP,2\n', '443,HTTPS,1\n']
        self.assertEqual(lines, expected_lines)

if __name__ == '__main__':
    unittest.main()
