"""This module test the function get_git_root"""
import unittest
import os
import git
import shutil

from scripts.functions.get_git_root import get_git_root


class TestGetGitRoot(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory to use as the Git repository
        self.temp_dir = os.path.join(os.path.dirname(__file__), 'tmp').replace('\\', '/')
        self.temp_repo = os.path.join(os.path.dirname(__file__), 'tmp/temp_repo').replace('\\', '/')
        os.mkdir(self.temp_dir)
        os.mkdir(self.temp_repo)
        git.Repo.init(self.temp_repo)

    def tearDown(self):
        # Cleanup the temporary directory
        if (os.path.isdir(self.temp_dir)):
            shutil.rmtree(self.temp_dir)

    def test_at_root_level(self):
        # Create a file within the Git repository
        test_file = os.path.join(self.temp_repo, 'test.txt')
        with open(test_file, 'w') as f:
            f.write('test')

        # Call the function and check the result
        self.assertEqual(get_git_root(test_file), self.temp_repo)

    def test_at_subfolder_level(self):
        git_subfolder = os.path.join(os.path.dirname(__file__), 'tmp/temp_repo/subfolder').replace('\\', '/')
        os.mkdir(git_subfolder)

        # Create a file within the Git repository
        test_file = os.path.join(git_subfolder, 'test.txt')
        with open(test_file, 'w') as f:
            f.write('test')

        # Call the function and check the result
        self.assertEqual(get_git_root(test_file), self.temp_repo)

    def test_non_git_dir(self):
        # Test that the function raises an exception for a non-git directory
        with self.assertRaises(git.exc.InvalidGitRepositoryError):
            get_git_root(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
