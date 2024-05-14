#!/usr/bin/env python
__author__ = "Damien Flament"
__contact__ = "damien.flament-sc@airliquide.com"
__copyright__ = "Copyright 2021, L'Air Liquide"
__date__ = "2021-12-23"
__maintainer__ = "Damien Flament"
__status__ = "Production"
__version__ = "1.2.0"

import os
import argparse
import yaml
import sys
import shutil
import git

parser = argparse.ArgumentParser(description='Copy docs and static')
parser.add_argument("--submodule-path", required=True, type=str, help="Documentation submodule path")
parser.add_argument("--docs-path", required=True, type=str, help="Documentation path")
parser.add_argument("--static-path", required=True, type=str, help="Static path")
parser.add_argument("--config-file", required=True, type=str, help="core_config path")
parser.add_argument("--test", required=True, type=str, help="Copy test docs only")
args = parser.parse_args()

submodule_root = args.submodule_path.strip('/') + '/'
docs_path = args.docs_path.strip('/') + '/'
static_project_path = args.static_path.strip('/') + '/' + 'prj/'
config_file = args.config_file
test_mode = args.test


def get_git_root(path):
    git_repo = git.Repo(path, search_parent_directories=True)
    return git_repo.git.rev_parse('--show-toplevel')


def rm_dir_keep_root(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    if not os.path.isdir(path):
        os.mkdir(path)


# Calculate relative path from root
ROOT_PATH = get_git_root('./') + '/'

config = yaml.load(open(config_file), Loader=yaml.FullLoader)

# Clean folders
rm_dir_keep_root(ROOT_PATH + docs_path)
rm_dir_keep_root(ROOT_PATH + static_project_path)

if (test_mode.lower() == 'true'):
    # Copy test docs
    slug = 'test/'
    if os.path.isdir(ROOT_PATH + submodule_root + slug + 'docs'):
        shutil.copytree(ROOT_PATH + submodule_root + slug + 'docs', ROOT_PATH + docs_path + slug)

    # Copy test static
    if os.path.isdir(ROOT_PATH + submodule_root + slug + 'static'):
        shutil.copytree(ROOT_PATH + submodule_root + slug + 'static', ROOT_PATH + static_project_path + slug)

else:
    # Copy docs and static
    for project in config:
        if (config[project]['enable'] is True):
            print('\n' + project)

            submodule = config[project]['submodule']
            if submodule is None or submodule == '':
                print('Can not find submodule, check ' + config_file)
                sys.exit(1)

            slug = submodule + '/'
            print(ROOT_PATH + docs_path + slug)

            # Copy docs
            if os.path.isdir(ROOT_PATH + submodule_root + slug + 'docs'):
                shutil.copytree(ROOT_PATH + submodule_root + slug + 'docs', ROOT_PATH + docs_path + slug)

            # Copy static
            if os.path.isdir(ROOT_PATH + submodule_root + slug + 'static'):
                shutil.copytree(ROOT_PATH + submodule_root + slug + 'static', ROOT_PATH + static_project_path + slug)

        else:
            print('\n' + project + ' (disabled)')
