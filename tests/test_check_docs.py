import unittest
import sys
import os

sys.path.append(f"{os.getcwd()}/scripts")

import check_docs


class TestGetGitRoot(unittest.TestCase):
    def setUp(self):
        self.work_dir = os.path.dirname(__file__)
        self.files_path = self.get_full_path('files')
        self.base_path_length = len(self.work_dir) + 1

    def test_list_markdown_files(self):
        expect = [
            self.get_full_path('files/nested_folder/file1.md'),
            self.get_full_path('files/nested_folder/file2.mdx'),
            self.get_full_path('files/carriage_return_cr.md'),
            self.get_full_path('files/carriage_return_crlf.md'),
            self.get_full_path('files/carriage_return_lf.md'),
            self.get_full_path('files/carriage_return_mixed.md'),
            self.get_full_path('files/dummy.md'),
            self.get_full_path('files/encoding_non_utf8.md'),
            self.get_full_path('files/encoding_utf8.md'),
        ]
        self.assertEqual(sorted(check_docs.list_markdown_files(self.files_path)), sorted(expect))

    def test_run_checks(self):
        given = [
            self.get_full_path('files/carriage_return_cr.md'),
            self.get_full_path('files/carriage_return_crlf.md'),
            self.get_full_path('files/carriage_return_lf.md'),
            self.get_full_path('files/carriage_return_mixed.md'),
        ]

        expect = [
            {"display_path": "files/carriage_return_cr.md", "pass_carriage_return": False, "pass_encoding": True},
            {"display_path": "files/carriage_return_crlf.md", "pass_carriage_return": False, "pass_encoding": True},
            {"display_path": "files/carriage_return_lf.md", "pass_carriage_return": True, "pass_encoding": True},
            {"display_path": "files/carriage_return_mixed.md", "pass_carriage_return": False, "pass_encoding": True},
        ]

        self.assertCountEqual(check_docs.run_checks(given, self.base_path_length), expect)

    def get_full_path(self, file_path: str) -> str:
        return os.path.join(self.work_dir, file_path).replace('\\', '/')
