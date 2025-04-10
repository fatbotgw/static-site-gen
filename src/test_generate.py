import unittest

from generate import extract_title, generate_page

class TestGenerate(unittest.TestCase):
    def test_extract_title(self):
        header = "# Hello World"

        self.assertEqual(extract_title(header), "Hello World")
        self.assertEqual(extract_title(header + "   "), "Hello World")

    def test_extract_title_h2(self):
        header = "## Hello World"
        with self.assertRaises(Exception):
            extract_title(header)

    def test_extract_title_no_header(self):
        header = "Hello World"
        with self.assertRaises(Exception):
            extract_title(header)
