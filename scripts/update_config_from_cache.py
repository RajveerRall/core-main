#!/usr/bin/env python
__author__ = "Damien Flament"
__contact__ = "damien.flament-sc@airliquide.com"
__copyright__ = "Copyright 2021, L'Air Liquide"
__date__ = "2021-12-10"
__maintainer__ = "Damien Flament"
__status__ = "Production"
__version__ = "1.4.0"

import argparse
import yaml
import json

# Configuration variable
api_url = "https://git.apps.airliquide.com/api/v4/"

parser = argparse.ArgumentParser(description='Generate json file with project edit url prefix')
parser.add_argument("--get", required=True, type=str, help="edit_url or service_desk_address")
parser.add_argument("--config-file", required=True, type=str, help="core_config path")
parser.add_argument("--destination-folder", required=True, type=str, help="Destination folder for json file")
parser.add_argument("--project-id", required=False, type=str, help="Documentation project ID")
parser.add_argument("--branch", required=False, type=str, help="Working branch")

args = parser.parse_args()

node = args.get
config_file = args.config_file
destination_folder = args.destination_folder
working_project_id = args.project_id
working_branch = args.branch

config = yaml.load(open(config_file), Loader=yaml.FullLoader)

items = {}
for project in config:
    if (config[project]['enable'] is True):
        project_id = project.split('_')[1]
        print('project id: ' + project_id)

        submodule_name = config[project].get('submodule')

        submodule_path = submodule_name

        ref_name = config[project].get('ref')
        item = config[project]['cache'].get(node)

        if (node == 'edit_url'):
            if working_project_id == project_id:
                item = item + working_branch + '/'
            else:
                item = item + 'main/'

        # Create dictionary
        items[submodule_path] = item

with open(destination_folder + node + '.json', 'w') as jsonFile:
    json.dump(items, jsonFile)
