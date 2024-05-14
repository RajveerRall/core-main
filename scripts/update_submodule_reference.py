#!/usr/bin/env python
__author__ = "Damien Flament"
__contact__ = "damien.flament-sc@airliquide.com"
__copyright__ = "Copyright 2021, L'Air Liquide"
__date__ = "2021-11-05"
__maintainer__ = "Damien Flament"
__status__ = "Production"
__version__ = "1.2.0"

import argparse
import ruamel.yaml

parser = argparse.ArgumentParser(description='Update submodule reference')
parser.add_argument("--project-id", required=True, type=str, help="Documentation project ID")
parser.add_argument("--forked-project-id", required=False, type=str, help="Forked documentation project ID")
parser.add_argument("--reference", required=True, type=str, help="Documentation path")
parser.add_argument("--config-file", required=True, type=str, help="core_config path")
args = parser.parse_args()

project_id = args.project_id
forked_project_id = args.forked_project_id
reference = args.reference
config_file = args.config_file

yaml = ruamel.yaml.YAML()
yaml.indent(mapping=2, sequence=2, offset=0)
yaml.preserve_quotes = True
yaml.width = float("inf")
yaml_file = open(config_file)

config = yaml.load(yaml_file)

config['project_' + project_id]['ref'] = reference

if forked_project_id:
    # Update project key when pipeline runs on a forked project
    config['project_' + forked_project_id] = config['project_' + project_id]
    del config['project_' + project_id]

with open(config_file, 'w') as yamlFile:
    yaml.dump(config, yamlFile)
