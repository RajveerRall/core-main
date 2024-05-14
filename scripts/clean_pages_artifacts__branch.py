#!/usr/bin/env python
__author__ = "Simon Torrez"
__contact__ = "simon.torrez@airliquide.com"
__copyright__ = "Copyright 2021, L'Air Liquide"
__date__ = "2022-05-13"
__maintainer__ = "Damien Flament"
__status__ = "Production"
__version__ = "1.2.0"

import argparse
import sys
import os
import shutil
import git


def parse_args():
    parser = argparse.ArgumentParser(
        description="Function to clean pages cache regarding branch state : removed branch --> removing associated cache")
    parser.add_argument("--branch-cache-folder", required=True, help="Path to the folder where cached asset belong")
    return parser.parse_args()


def main():
    args = parse_args()
    root_cache_folder = args.branch_cache_folder

    branches = []
    git_repo = git.Repo('.', search_parent_directories=True)
    git_repo.remote().update()
    remote_refs = git_repo.remote().refs
    for refs in remote_refs:
        print('Existing branches:')
        print(refs.name)
        if refs.name != 'origin/HEAD':
            branches.append(refs.name[7:])  # Remove origin/

    # Get orphaned cache folders in /public/branch
    try:
        folders = os.listdir(path=root_cache_folder)
        cache_folder_to_remove = list(set(folders) - set(branches))
    except FileNotFoundError:
        print(f'Folder {root_cache_folder} is absent cache')
        cache_folder_to_remove = False
    except Exception:
        print(f'Get orphaned cache in {root_cache_folder}')
        print('Unexpected error:', sys.exc_info()[0])
        sys.exit(1)

    # Remove orphaned cache folders in /public/branch
    if cache_folder_to_remove:
        try:
            print("There is some folders in cache to clean")
            for folder in cache_folder_to_remove:
                print(f'Removing cache folder: {root_cache_folder}/{folder}')
                shutil.rmtree(f'{root_cache_folder}/{folder}')
        except Exception:
            print(f'Remove orphaned cache folder in {root_cache_folder}')
            print('Unexpected error:', sys.exc_info()[0])
            sys.exit(1)


if __name__ == '__main__':
    main()
