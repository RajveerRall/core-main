#!/usr/bin/env python
__author__ = "Damien Flament"
__contact__ = "damien.flament-sc@airliquide.com"
__copyright__ = "Copyright 2021, Air Liquide"
__date__ = "2021-12-07"
__maintainer__ = "Damien Flament"
__status__ = "Production"
__version__ = "1.1.0"

import json
import yaml
import argparse
import uuid


def add_ids(data):
    if isinstance(data, dict):
        data['id'] = str(uuid.uuid4())
        for key in data:
            if isinstance(data[key], (dict, list)):
                add_ids(data[key])
    elif isinstance(data, list):
        for obj in data:
            if isinstance(obj, (dict, list)):
                add_ids(obj)


parser = argparse.ArgumentParser(description='Extract yaml element to json file')
parser.add_argument("--config-file", required=True, type=str, help="Landing page configuration file")
parser.add_argument("--element", required=True, type=str, help="Json element")
parser.add_argument("--keep-root", required=True, type=str, help="Keep root element")
parser.add_argument("--add-id", required=True, type=str, help="Add id to objects")
parser.add_argument("--destination-file", required=True, type=str, help="Destination json file")
args = parser.parse_args()

config_file = args.config_file
element = args.element
keep_root = args.keep_root
add_id = args.add_id
destination_file = args.destination_file

element_config = yaml.safe_load(open(config_file))[element]

if add_id == 'true':
    add_ids([element_config])

with open(destination_file, 'w') as jsonFile:
    if keep_root == 'true':
        json.dump({element: element_config}, jsonFile)
    else:
        json.dump(element_config, jsonFile)
