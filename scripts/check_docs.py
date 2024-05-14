#!/usr/bin/env python
__author__ = "Damien Flament"
__contact__ = "damien.flament-sc@airliquide.com"
__copyright__ = "Copyright 2021, L'Air Liquide"
__date__ = "2021-12-28"
__maintainer__ = "Damien Flament"
__status__ = "Production"
__version__ = "1.3.0"

import os
import argparse
import yaml
import sys
# Module python-frontmatter (not frontmatter)

from functions.get_git_root import get_git_root
from classes.DocChecker import DocChecker


def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments for the `check_docs.py` script.

    :returns: An `argparse.Namespace` object containing the parsed command-line arguments.
    :rtype: argparse.Namespace

    **Usage**

    `check_docs.py [-h] [--docs-path DOCS_PATH] | [--submodule-path SUBMODULE_PATH] [--config-file CONFIG_FILE] [--test TEST]`

    **Description**

    This function creates an `ArgumentParser` object to parse command-line arguments for the `check_docs.py` script.
    The parser is used to parse the `--docs-path` argument, if provided, or the `--submodule-path`, `--config-file`, and `--test`
    arguments if `--docs-path` is not provided.

    **Arguments**

    There are three possible command-line arguments that can be parsed by this function:

    * `--docs-path`: (optional) A string representing the path to the directory containing the `.md` and `.mdx` files to be checked.
    * `--submodule-path`: (required if `--docs-path` is not provided) A string representing the path to the submodule within the core project.
    * `--config-file`: (required if `--docs-path` is not provided) A string representing the path to the configuration file.
    * `--test`: (required if `--docs-path` is not provided) A boolean indicating whether to check test docs only.

    :raises: `ArgumentError` if the required arguments are not provided.
    """
    parser = argparse.ArgumentParser(
        usage='check_docs.py [--submodule-path SUBMODULE_PATH] [--config-file CONFIG_FILE]', description='Check docs for common errors')
    parser.add_argument("--submodule-path", required=True, type=str, help="Documentation path")
    parser.add_argument("--config-file", required=True, type=str, help="core_config path")
    parser.add_argument("--test", required=True, type=str, help="Check test docs only")
    return parser.parse_args()


def main() -> None:
    """
    The main function for the `check_docs.py` script.

    :returns: None
    :raises: Any exceptions raised by the `parse_args`, `run_on_docs_project`, or `run_on_core_project` functions.

    **Description**

    This function is the entry point for the `check_docs.py` script. It first parses the command-line arguments using the `parse_args` function.

    The function sets the global variable `ROOT_PATH` to the root directory
        of the Git repository that contains the specified path, using the `get_git_root` function.

    :raises: Any exceptions raised by the `parse_args`, `run_on_docs_project`, or `run_on_core_project` functions.
    """
    global ROOT_PATH
    args = parse_args()
    submodule_root = args.submodule_path.strip('/') + '/'
    config_file = args.config_file
    test_mode = args.test

    # Calculate relative path from root
    ROOT_PATH = get_git_root('./') + '/'

    if (test_mode.lower() == 'true'):
        slug = 'test/'
        docs_full_path = ROOT_PATH + submodule_root + slug + 'docs'
        base_path_length = len(ROOT_PATH + submodule_root + slug)
        run_checks(list_markdown_files(docs_full_path), base_path_length)

    else:
        config = yaml.load(open(config_file), Loader=yaml.FullLoader)

        for project in config:
            if config[project]['enable']:
                print('\n' + project)

                submodule = config[project]['submodule']
                if submodule is None or submodule == '':
                    # TODO remove this check, validate config instead
                    print('Can not find submodule, check ' + config_file)
                    sys.exit(1)

                slug = submodule + '/'
                docs_full_path = ROOT_PATH + submodule_root + slug + 'docs'
                base_path_length = len(ROOT_PATH + submodule_root + slug)

                print(slug)
                run_checks(list_markdown_files(docs_full_path), base_path_length)

            else:
                print('\n' + project + ' (disabled)')


def list_markdown_files(path: str) -> list:
    """
    Get a list of all `.md` and `.mdx` files in the specified path.

    :param path: A string representing the path to the directory containing the `.md` and `.mdx` files to be checked.
    :return: A list of strings representing the full path to each `.md` and `.mdx` file found in the specified directory.
    """
    return [os.path.join(root, file).replace('\\', '/') for root, dirs, files in os.walk(path) for file in files if file.endswith(('.md', '.mdx'))]


def run_checks(files_path: list, base_path_length: int) -> list:
    """
    Run all checks on the specified files.

    :param files_path: A list of strings representing the full paths to the files being checked.
    :type files_path: List[str]
    :param base_path_length: An integer representing the length of the base path.
    :type base_path_length: int
    :returns: A list of `DocChecker` objects representing the results of the checks.
    :rtype: List[DocChecker]
    :raises: Any exceptions raised by the `validate_carriage_return` or `validate_encoding` functions.
    """
    files_checks = []
    for file_path in files_path:
        doc = DocChecker(file_path, file_path[base_path_length:].replace('\\', '/'))
        files_checks.append({
            "display_path": doc.display_path,
            "pass_carriage_return": doc.validate_carriage_return(),
            "pass_encoding": doc.validate_encoding()
        })

    return files_checks

    # TODO test if doc_version is present
    # TODO test if doc_version is date (format 2022-07-27) or version (format v1.2.3)


if __name__ == '__main__':
    main()
