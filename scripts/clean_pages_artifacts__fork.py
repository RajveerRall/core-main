#!/usr/bin/env python
__author__ = "Damien Flament"
__contact__ = "damien.flament-sc@airliquide.com"
__copyright__ = "Copyright 2021, L'Air Liquide"
__date__ = "2022-09-22"
__maintainer__ = "Damien Flament"
__status__ = "Production"
__version__ = "1.0.0"

import argparse
import requests
import json
import sys
import os
import shutil

# Configuration variable
api_url = "https://git.apps.airliquide.com/api/v4/"


def parse_args():
    """
    _summary_

    :return: _description_
    :rtype: _type_
    """
    parser = argparse.ArgumentParser(
        description="Function to clean pages cache regarding merge request state: closed/merged merge request --> removing associated cache")
    parser.add_argument("--project-id", required=True, type=str, help="Current project ID")
    parser.add_argument("--fork-cache-folder", required=True, help="Path to the folder where cached asset belong")

    return parser.parse_args()


class Project():
    def __init__(self, project_id, api_url):
        response = requests.get(f'{api_url}projects/{project_id}/merge_requests?state=opened')
        self.response = json.loads(response.text)

    def get_merge_request_iid(self) -> list:
        mr_list = []
        for mr in self.response:
            mr_list.append(f"{mr['iid']}")
        return mr_list


def main():
    args = parse_args()
    project_id = args.project_id
    root_cache_folder = args.fork_cache_folder

    project = Project(project_id, api_url)
    merge_requests = project.get_merge_request_iid()

    # Get orphaned cache folders in /public/fork using merge request iid prefix
    try:
        folders = os.listdir(path=root_cache_folder)
        cache_folder_prefix_to_remove = list(set(i.split('-')[0] for i in folders) - set(merge_requests))
    except FileNotFoundError:
        print(f'Folder {root_cache_folder} is absent from cache')
        cache_folder_prefix_to_remove = False
    except Exception:
        print(f'Get orphaned cache in {root_cache_folder}')
        print('Unexpected error:', sys.exc_info()[0])
        sys.exit(1)

    # Select full folder name to remove from folder prefix
    cache_folder_to_remove = []
    if cache_folder_prefix_to_remove:
        folders = os.listdir(path=root_cache_folder)
        for folder in folders:
            if folder.split('-')[0] in cache_folder_prefix_to_remove:
                cache_folder_to_remove.append(folder)
    else:
        cache_folder_to_remove = False

    # Remove orphaned cache folders in /public/fork
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
