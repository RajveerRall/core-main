#!/usr/bin/env python
__author__ = "Damien Flament"
__contact__ = "damien.flament-sc@airliquide.com"
__copyright__ = "Copyright 2021, Air Liquide"
__date__ = "2021-12-07"
__maintainer__ = "Damien Flament"
__status__ = "Production"
__version__ = "1.3.2"

import argparse
import yaml
import sys
import re
import os
import os.path as path

parser = argparse.ArgumentParser(description='Configure docusaurus sidebars')
parser.add_argument("--submodule-path", required=True, type=str, help="Documentation submodule path")
parser.add_argument("--config-file", required=True, type=str, help="core_config path")
parser.add_argument("--manifest", required=True, type=str, help="Path to sidebars.js file")
parser.add_argument("--test", required=True, type=str, help="Generate sidebars for test only")
args = parser.parse_args()

submodule_root = args.submodule_path.strip('/') + '/'
config_file = args.config_file
manifest = args.manifest
test_mode = args.test


def walk(top, topdown=True, onerror=None, followlinks=False, maxdepth=None):
    islink, join, isdir = path.islink, path.join, path.isdir

    try:
        names = os.listdir(top)
    except OSError as err:
        if onerror is not None:
            onerror(err)
        return

    dirs, nondirs = [], []
    for name in names:
        if isdir(join(top, name)):
            dirs.append(name)
        else:
            nondirs.append(name)

    if topdown:
        yield top, dirs, nondirs

    if maxdepth is None or maxdepth > 1:
        for name in dirs:
            new_path = join(top, name)
            if followlinks or not islink(new_path):
                for x in walk(new_path, topdown, onerror, followlinks, None if maxdepth is None else maxdepth - 1):
                    yield x
    if not topdown:
        yield top, dirs, nondirs


config = yaml.load(open(config_file), Loader=yaml.FullLoader)

if not path.isfile(manifest):
    print(f'Manifest file not found: {manifest}')
    sys.exit(1)

sidebars = open(manifest).read()

if (test_mode.lower() == 'true'):
    project_sidebar_config = "  'test': [{type: 'autogenerated', dirName: 'test'}],"

else:
    project_sidebar_config = ''
    for project in config:
        if (config[project]['enable'] is True):
            if config[project]['sidebar']['level'] == 0:
                project_sidebar_config = project_sidebar_config + '  \'' + \
                    config[project]['submodule'] + '\': [{type: \'' + config[project]['sidebar']['type'] + \
                    '\', dirName: \'' + config[project]['submodule'] + '\'}],\n'
            else:
                for root, dirnames, filenames in walk(submodule_root + config[project]['submodule'] + '/docs', maxdepth=config[project]['sidebar']['level']):
                    for dir in dirnames:
                        sidebar_folder = (config[project]['submodule'] + root[len(submodule_root + config[project]
                                          ['submodule'] + '/docs'):] + '/' + dir).replace('\\', '/')
                        project_sidebar_config = project_sidebar_config + '  \'' + sidebar_folder + \
                            '\': [{type: \'' + config[project]['sidebar']['type'] + '\', dirName: \'' + sidebar_folder + '\'}],\n'

sidebars = re.sub(r'(?i)module.exports = {', 'module.exports = {\n' + project_sidebar_config, sidebars)

f = open(manifest, "w")
f.write(sidebars)
f.close()
