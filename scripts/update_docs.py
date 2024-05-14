#!/usr/bin/env python
__author__ = "Damien Flament"
__contact__ = "damien.flament-sc@airliquide.com"
__copyright__ = "Copyright 2021, L'Air Liquide"
__date__ = "2021-12-27"
__maintainer__ = "Damien Flament"
__status__ = "Production"
__version__ = "1.5.0"

import os
import argparse
import yaml
import sys
# Module python-frontmatter (not frontmatter)
import frontmatter
import io
import git
import re

parser = argparse.ArgumentParser(description='Update links and image path')
parser.add_argument("--docs-path", required=True, type=str, help="Documentation path")
parser.add_argument("--base-url", required=True, type=str, help="Base URL")
parser.add_argument("--config-file", required=True, type=str, help="core_config path")
parser.add_argument("--build", required=True, type=str, help="production or preview")
args = parser.parse_args()

submodule_path = 'docs/'  # Where documentation submodule are stored
docs_md_path = 'docs/'  # Where md and mdx files are stored within the documentation repository
docs_path = args.docs_path.strip('/') + '/'
base_url = args.base_url.lstrip()
config_file = args.config_file
build = args.build


def get_git_root(path):
    git_repo = git.Repo(path, search_parent_directories=True)
    return git_repo.git.rev_parse('--show-toplevel')


# Calculate relative path from root
ROOT_PATH = get_git_root('./') + '/'

config = yaml.load(open(config_file), Loader=yaml.FullLoader)

# Add slug when needed in:
#   - Frontmatter
#   - Links
#   - Images
for project in config:
    if (config[project]['enable'] is True):
        print('\n' + project)

        submodule = config[project]['submodule']
        if submodule is None or submodule == '':
            print('Can not find submodule, check ' + config_file)
            sys.exit(1)

        slug = submodule + '/'

        lnk_prefix = "/" + submodule
        img_prefix = "/prj/" + submodule

        # base_url
        # print(ROOT_PATH + docs_path + slug)

        print('base_url:            ' + base_url)
        print('lnk_prefix:          ' + lnk_prefix)
        print('img_prefix:          ' + img_prefix)

        # Documentation repository path
        doc_repo = git.Git(ROOT_PATH + submodule_path + slug)
        print('doc_repo path:       ' + ROOT_PATH + submodule_path + slug)
        print('img_prefix:          ' + img_prefix)

        # Loop on all md an d mdx files in current slug
        for root, dirs, files in os.walk(ROOT_PATH + docs_path + slug):
            for file in files:
                if file.endswith(('.md', '.mdx')):
                    file_path = os.path.join(root, file).replace('\\', '/')  # Path at target

                    # Read doc file
                    with io.open(file_path, 'r', encoding='utf-8') as f:
                        doc_file = frontmatter.load(f, encoding='utf-8', handler=None)
                        f.close()

                    if (build.lower() == 'production'):
                        # Same file in source submodule repository
                        repo_file_path = docs_md_path + os.path.join(root, file).replace('\\', '/')[len(ROOT_PATH + docs_path + slug):]
                        print('repo_file_path:      ' + repo_file_path)

                        # Fetch last_update_date and last_update_author
                        git_log = doc_repo.log('-n 1', '--date=iso', '--format=%cd%n%an', '--', repo_file_path).split('\n')
                        if len(git_log) != 2:
                            git_log = None
                        last_update_date = None
                        last_update_author = None
                        try:
                            last_update_date = git_log[0]
                            # print('last_update_date:    ' + last_update_date)
                        except Exception:
                            print('last_update_date:    ERROR')
                        try:
                            last_update_author = git_log[1]
                            # print('last_update_author:  ' + last_update_author)
                        except Exception:
                            print('last_update_author:  ERROR')

                    # 1 - Frontmatter update
                        # last_update (force if defined)
                        if last_update_date is not None or last_update_author is not None:
                            doc_file['last_update'] = {}
                            if last_update_date is not None:
                                doc_file['last_update']['date'] = last_update_date
                            if last_update_author is not None:
                                doc_file['last_update']['author'] = last_update_author

                    # slug (update only)
                    try:
                        doc_file['slug'] = lnk_prefix + doc_file['slug']
                    except KeyError:
                        # No slug attribute
                        pass
                    except Exception as ex:
                        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                        message = template.format(type(ex).__name__, ex.args)
                        print(message)

                    # 3 - Root relative link update
                    #     -> Must be executed before slug relative link update
                    regex = r"(?<!!)\[(.*)\]\((?:(?![a-z][a-z0-9+\-.]*:))/(.*)\)"
                    subst = "[\\g<1>](/" + base_url.strip('/') + "\\g<2>)"
                    doc_file.content = re.sub(regex, subst, doc_file.content, 0)

                    # 2 - Slug relative link update
                    # regex = r"(?<!!)\[(.*)\]\((?:(?![a-z][a-z0-9+\-.]*:))(?:(?!/))(.*)\)"
                    # subst = "[\\g<1>](" + lnk_prefix + "/\\g<2>)"
                    # doc_file.content = re.sub(regex, subst, doc_file.content, 0)

                    # 4 - Image update (Markdown)
                    regex = r"(!\[.*\])\(([a-zA-Z0-9_\-\./]*)( .*)?\)"
                    subst = "\\g<1>(" + img_prefix + "/\\g<2>\\g<3>)"
                    doc_file.content = re.sub(regex, subst, doc_file.content, 0)

                    # 5 - Image update (HTML) - https://regex101.com/r/3YfR6g/1
                    regex = r"<img(?P<attr1>(\n|.)*?)src=\"(?<!<http://)(?P<src>[a-zA-Z0-9_\-\./]*)\"(?P<attr2>(\n|.)*?)/>"
                    subst = "<img\\g<attr1>src=\"" + base_url.rstrip('/') + img_prefix + "/\\g<src>\" \\g<attr2>/>"
                    doc_file.content = re.sub(regex, subst, doc_file.content, 0)

                    # Write updated doc file
                    with io.open(file_path, 'wb') as updated_doc_file:
                        updated_doc_file.write(bytes(frontmatter.dumps(doc_file), "UTF-8"))
                        updated_doc_file.close()

    else:
        print('\n' + project + ' (disabled)')
