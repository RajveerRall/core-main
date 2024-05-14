#!/usr/bin/env python
__author__ = "Damien Flament"
__contact__ = "damien.flament-sc@airliquide.com"
__copyright__ = "Copyright 2021, L'Air Liquide"
__date__ = "2021-07-16"
__maintainer__ = "Damien Flament"
__status__ = "Production"
__version__ = "1.6.0"

import argparse
import yaml
import os
import subprocess
import git
import shlex

parser = argparse.ArgumentParser(description='Configure documentation submodule')
parser.add_argument("--submodule-path", required=True, type=str, help="Documentation submodule path")
parser.add_argument("--config-file", required=True, type=str, help="core_config path")
args = parser.parse_args()

SUBMODULE_ROOT = args.submodule_path
config_file = args.config_file


def get_git_root(path):
    repo = git.Repo(path, search_parent_directories=True)
    return repo.git.rev_parse('--show-toplevel')


def run(command_line):
    args = shlex.split(command_line)
    print('command: ' + ' '.join(args))
    result = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    print(result.stdout)


class Submodule:
    def __init__(self, project, config):
        self.name = config[project].get('submodule')
        self.path = SUBMODULE_ROOT + self.name
        self.url = config[project]['cache'].get('http_url_to_repo')
        self.ref = config[project].get('ref')

    def set_url(self):
        run(f'git -C {RELATIVE_PATH} submodule set-url -- {self.path} {self.url}')

    def update_index(self):
        run(f'git -C {RELATIVE_PATH} update-index --cacheinfo 160000 {self.ref} {self.path}')

    def add(self):
        git.Submodule.add(REPO, self.path, self.path, self.url)


# Calculate relative path from root
ROOT_PATH = get_git_root('./')
RELATIVE_PATH = ''
RELATIVE_LEVEL = os.getcwd().replace('\\', '/').count('/') - ROOT_PATH.count('/')
for i in range(RELATIVE_LEVEL):
    RELATIVE_PATH += '../'

# Def git repo
REPO = git.Repo(ROOT_PATH)

# Creating submodule root if needed
if os.path.isdir(RELATIVE_PATH + SUBMODULE_ROOT) is False:
    os.makedirs(RELATIVE_PATH + SUBMODULE_ROOT)

print('ROOT_PATH:     ' + ROOT_PATH)
print('RELATIVE_PATH: ' + RELATIVE_PATH)
print()


def main():
    config = yaml.load(open(config_file), Loader=yaml.FullLoader)

    # Update .gitmodule url and ref from core_config
    submodule_list = []
    for project in config:
        if (config[project]['enable'] is True):
            print(f'Updating submodule for {project}')
            submodule = Submodule(project, config)
            if submodule.path not in REPO.submodules:
                print(f'Submodule {submodule.path} does not exist, creating')
                submodule.add()
            submodule.set_url()
            submodule.update_index()

            # Add to submodule_list
            submodule_list.append(submodule.path)

    # Remove any submodule that not in submodule_list
    for sm in REPO.submodules:
        if sm.path not in submodule_list:
            print(f'Submodule {sm.path} exist but absent from config (or disabled), removing')
            REPO.submodule(sm.path).remove(True, True, True, False)

    # Init all submodules
    print('Initializing submodules')
    run(f'git -C {RELATIVE_PATH} submodule update --init')


if __name__ == "__main__":
    main()
