#!/usr/bin/env python
__author__ = "Damien Flament"
__contact__ = "damien.flament-sc@airliquide.com"
__copyright__ = "Copyright 2022, L'Air Liquide"
__date__ = "2022-09-20"
__maintainer__ = "Damien Flament"
__status__ = "Production"
__version__ = "1.0.0"


import argparse
from urllib.parse import urlparse
from ruamel.yaml import YAML
yaml = YAML()

parser = argparse.ArgumentParser(description='Update core config cache for all registered projects using API')
parser.add_argument("--project-id", required=True, type=str, help="Project ID to update")
parser.add_argument("--project-url", required=True, type=str, help="CI_PROJECT_URL")
parser.add_argument("--project-path-slug", required=True, type=str, help="CI_PROJECT_PATH_SLUG")
parser.add_argument("--job-token", required=True, type=str, help="CI_JOB_TOKEN")
parser.add_argument("--config-file", required=True, type=str, help="core_config path")

args = parser.parse_args()
project_id = args.project_id
job_token = args.job_token
project_url = args.project_url
project_path_slug = args.project_path_slug
config_file = args.config_file


class Project():
    """
    _summary_
    """

    def __init__(self, project_id, project_url, project_path_slug, job_token):
        """
        _summary_

        :param project_id: _description_
        :type project_id: _type_
        :param project_url: _description_
        :type project_url: _type_
        :param project_path_slug: _description_
        :type project_path_slug: _type_
        :param job_token: _description_
        :type job_token: _type_
        """
        self.project_id = project_id
        self.project_url = project_url
        self.project_path_slug = project_path_slug
        self.job_token = job_token

    def get_http_url_to_repo(self) -> str:
        """
        _summary_

        :return: _description_
        :rtype: str
        """
        uri = urlparse(self.project_url)
        return f'{uri.scheme}://gitlab-ci-token:{self.job_token}@{uri.netloc}{uri.path}.git'

    def get_web_url(self) -> str:
        """
        _summary_

        :return: _description_
        :rtype: str
        """
        return f'{self.project_url}/-/edit/'

    def get_service_desk_address(self) -> str:
        """
        _summary_

        :return: _description_
        :rtype: str
        """
        return f'gitlab+{self.project_path_slug}-{self.project_id}-issue-@airliquide.com'


def update_config(config, project_id, project_url, project_path_slug, job_token):
    """
    _summary_

    :param config: _description_
    :type config: _type_
    :param project_id: _description_
    :type project_id: _type_
    :param project_url: _description_
    :type project_url: _type_
    :param project_path_slug: _description_
    :type project_path_slug: _type_
    :param job_token: _description_
    :type job_token: _type_

    :return: _description_
    :rtype: _type_
    """
    print('project id: ' + project_id)
    project = Project(project_id, project_url, project_path_slug, job_token)

    print("http_url_to_repo:      " + project.get_http_url_to_repo())
    print("edit_url:              " + project.get_web_url())
    print("service_desk_address:  " + project.get_service_desk_address())
    print()

    try:
        config['project_' + project_id]['cache'].items()
    except Exception:
        config['project_' + project_id]['cache'] = {}

    config['project_' + project_id]['cache']['http_url_to_repo'] = project.get_http_url_to_repo()
    config['project_' + project_id]['cache']['edit_url'] = project.get_web_url()
    config['project_' + project_id]['cache']['service_desk_address'] = project.get_service_desk_address()

    return config


def main():
    config = yaml.load(open(config_file))
    yaml.width = 180

    config = update_config(config, project_id, project_url, project_path_slug, job_token)

    with open(config_file, 'w') as fp:
        yaml.dump(config, fp)


if __name__ == "__main__":
    main()
