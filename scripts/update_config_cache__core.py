#!/usr/bin/env python
__author__ = "Damien Flament"
__contact__ = "damien.flament-sc@airliquide.com"
__copyright__ = "Copyright 2022, L'Air Liquide"
__date__ = "2022-07-26"
__maintainer__ = "Damien Flament"
__status__ = "Production"
__version__ = "1.2.0"


import argparse
import requests
import json
from ruamel.yaml import YAML
yaml = YAML()

parser = argparse.ArgumentParser(description='Update core config cache for all registered projects using API')
parser.add_argument("--read-token", required=True, type=str, help="READ_API_TOKEN")
parser.add_argument("--config-file", required=True, type=str, help="core_config path")

args = parser.parse_args()

read_token = args.read_token
config_file = args.config_file

# Configuration variable
api_url = "https://git.apps.airliquide.com/api/v4/"


class Project():
    def __init__(self, project_id, api_url, read_token):
        headers = {"PRIVATE-TOKEN": read_token}
        response = requests.get(api_url + "projects/" + project_id, headers=headers)
        self.response = json.loads(response.text)
        self.id = project_id

    def get_http_url_to_repo(self) -> str:
        return self.response.get('http_url_to_repo')

    def get_web_url(self) -> str:
        return self.response.get('web_url') + '/-/edit/'

    def get_service_desk_address(self) -> str:
        return self.response.get('service_desk_address')


def update_config(config, project):
    print('project_id: ' + project.id)

    print("http_url_to_repo:      " + project.get_http_url_to_repo())
    print("edit_url:              " + project.get_web_url())
    print("service_desk_address:  " + project.get_service_desk_address())
    print()

    try:
        config['project_' + project.id]['cache'].items()
    except Exception:
        config['project_' + project.id]['cache'] = {}

    config['project_' + project.id]['cache']['http_url_to_repo'] = project.get_http_url_to_repo()
    config['project_' + project.id]['cache']['edit_url'] = project.get_web_url()
    config['project_' + project.id]['cache']['service_desk_address'] = project.get_service_desk_address()

    return config


def main():
    config = yaml.load(open(config_file))
    yaml.width = 180

    for project in config:
        config = update_config(config, Project(project.split('_')[1], api_url, read_token))

    with open(config_file, 'w') as fp:
        yaml.dump(config, fp)


if __name__ == "__main__":
    main()
