"""This module test the function get_git_root"""
import unittest
import os

from scripts.classes.DocChecker import DocChecker


class TestDocChecker(unittest.TestCase):
    def setUp(self):
        self.work_dir = os.path.dirname(__file__)
        self.dummy_file = self.get_full_path('files/dummy.md')

    def test_display_path(self):
        self.assertTrue(DocChecker(self.dummy_file, 'dummy.md').validate_carriage_return())

    def test_method_repr(self):
        self.assertRegex(DocChecker(self.dummy_file, '').__repr__(), r'.*dummy\.md.*')

    def test_method_str(self):
        self.assertRegex(DocChecker(self.dummy_file, '').__str__(), r'.*dummy\.md.*')

    def test_carriage_return_lf(self):
        file_path = self.get_full_path('files/carriage_return_lf.md')
        self.write_file(file_path, ['# LF carriage return test file\n', '\n', '\n'])
        self.assertTrue(DocChecker(file_path, '').validate_carriage_return())

    def test_carriage_return_crlf(self):
        file_path = self.get_full_path('files/carriage_return_crlf.md')
        self.write_file(file_path, ['# CRLF carriage return test file\r\n', '\r\n', '\r\n'])
        self.assertFalse(DocChecker(file_path, '').validate_carriage_return())

    def test_carriage_return_cr(self):
        file_path = self.get_full_path('files/carriage_return_cr.md')
        self.write_file(file_path, ['# CR carriage return test file\r', '\r', '\r'])
        self.assertFalse(DocChecker(file_path, '').validate_carriage_return())

    def test_carriage_return_mixed(self):
        file_path = self.get_full_path('files/carriage_return_mixed.md')
        self.write_file(file_path, ['# Mixed carriage return test file\r', '\r', '\n'])
        self.assertFalse(DocChecker(file_path, '').validate_carriage_return())

    def test_encoding_utf8(self):
        file_path = self.get_full_path('files/encoding_utf8.md')
        self.assertTrue(DocChecker(file_path, '').validate_encoding())

    def test_encoding_non_utf8(self):
        file_path = self.get_full_path('files/encoding_non_utf8.md')
        self.assertFalse(DocChecker(file_path, '').validate_encoding())

    def get_full_path(self, file_path: str) -> str:
        return os.path.join(self.work_dir, file_path).replace('\\', '/')

    def write_file(self, file_path: str, lines: list) -> None:
        with open(file_path, "wb") as fhandle:
            for line in lines:
                fhandle.write(line.encode("utf-8"))
