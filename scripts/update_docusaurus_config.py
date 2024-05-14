#!/usr/bin/env python
__author__ = "Damien Flament"
__contact__ = "damien.flament-sc@airliquide.com"
__copyright__ = "Copyright 2021, Air Liquide"
__date__ = "2021-10-25"
__maintainer__ = "Damien Flament"
__status__ = "Production"
__version__ = "1.3.2"

import sys
import argparse
import re
from os import path

parser = argparse.ArgumentParser(description='Update url and baseUrl from docusaurus.config.js file')
parser.add_argument("--url", required=True, type=str, help="url")
parser.add_argument("--base-url", required=True, type=str, help="baseUrl")
parser.add_argument("--production", required=True, type=str, help="Display test banner true/false")
parser.add_argument("--manifest", required=True, type=str, help="Path to docusaurus.config.js file")
parser.add_argument("--test", required=True, type=str, help="Allow build with broken link for testing purpose")
args = parser.parse_args()

url = args.url
base_url = args.base_url.lstrip()
production = args.production
manifest = args.manifest
test_mode = args.test

if not path.isfile(manifest):
    print(f'Manifest file not found: {manifest}')
    sys.exit(1)

cfg = open(manifest).read()

# Detect indentation
indent = re.search(r'(?im)^(?P<indent>\s*)themeConfig: {', cfg).groupdict()['indent']

# test
if (test_mode.lower() == 'true'):
    cfg = re.sub(r'(?ims)^(?P<indent>\s*)onBrokenLinks: \".*?\",\n', r'\g<indent>onBrokenLinks: "warn",\n', cfg)
    cfg = re.sub(r'(?ims)^(?P<indent>\s*)onBrokenMarkdownLinks: \".*?\",\n', r'\g<indent>onBrokenMarkdownLinks: "warn",\n', cfg)

    announcement_bar = '''  {indent}announcementBar: {{
    {indent}id: "non_production",
    {indent}content: "You are browsing a test version of this site.",
    {indent}backgroundColor: "#cc0000",
    {indent}textColor: "#ffe9d9",
    {indent}isCloseable: false,
  {indent}}},'''

    test_navbar = '''    {indent}//test-navbar-start
    {indent}title: "Test Guides",
    {indent}logo: {{
      {indent}alt: "Test Guides",
      {indent}src: "img/favicon.ico",
    {indent}}},
    {indent}items: [
      {indent}{{
        {indent}label: "Test",
        {indent}position: "left",
        {indent}items: [
          {indent}{{
            {indent}label: "Test",
            {indent}to: "docs/test/",
          {indent}}}
        {indent}],
      {indent}}},
    {indent}],
    {indent}hideOnScroll: true,
    {indent}//test-navbar-end'''

    if (not re.search(r'(?im)^\s+//test-navbar-start$', cfg)):
        # Test navbar not present, adding it
        test_navbar = test_navbar.format(indent=indent)
        cfg = re.sub(r'(?i)(?P<indent>\s*)navbar: {', r'\g<indent>navbar: {\n' + test_navbar, cfg)

        # Comment production navbar
        producation_navbar = re.search(r'(?is)\s+//test-navbar-end\s(?P<navbar>.*,)\s+},\s+footer: {', cfg).groupdict()['navbar']

        producation_navbar_comment = ''
        for line in producation_navbar.splitlines():
            producation_navbar_comment = producation_navbar_comment + indent + '    //' + line[len(indent) + 4:] + '\n'
        producation_navbar_comment = '\n'.join(producation_navbar_comment.split('\n')[:-1])  # Remove last empty line

        cfg = re.sub(r'(?is)(\s+//test-navbar-end\s).*,(\s+},\s+footer: {)', r'\1' + producation_navbar_comment + r'\2', cfg)

else:
    cfg = re.sub(r'(?ims)^(?P<indent>\s*)onBrokenLinks: \".*?\",\n', r'\g<indent>onBrokenLinks: "throw",\n', cfg)
    cfg = re.sub(r'(?ims)^(?P<indent>\s*)onBrokenMarkdownLinks: \".*?\",\n', r'\g<indent>onBrokenMarkdownLinks: "throw",\n', cfg)

    announcement_bar = '''  {indent}announcementBar: {{
    {indent}id: "non_production",
    {indent}content: "You are browsing a non production version of this site.",
    {indent}backgroundColor: "#b36119",
    {indent}textColor: "#ffe9d9",
    {indent}isCloseable: false,
  {indent}}},'''

    if (re.search(r'(?im)^\s+//test-navbar-start$', cfg)):
        # Test navbar is present, removing it
        cfg = re.sub(r'(?is)\s+//test-navbar-start\s(.*),\s+\s+//test-navbar-end', '', cfg)

        # Uncomment production navbar
        producation_navbar_comment = re.search(r'(?is)\s+navbar: {\s(?P<navbar>.*,)\s+},\s+footer: {', cfg).groupdict()['navbar']

        producation_navbar = ''
        for line in producation_navbar_comment.splitlines():
            producation_navbar = producation_navbar + indent + '    ' + line[len(indent) + 6:] + '\n'
        producation_navbar = '\n'.join(producation_navbar.split('\n')[:-1])  # Remove last empty line

        cfg = re.sub(r'(?is)(\s+navbar: {\s).*,(\s+},\s+footer: {)', r'\1' + producation_navbar + r'\2', cfg)

# url
cfg = re.sub(r'(?i) {2}url: ".+",', '  url: "' + url + '",', cfg)
cfg = re.sub(r'(?i) {2}baseUrl: ".+",', '  baseUrl: "' + base_url + '",', cfg)

# announcementBar
if (production.lower() == 'false' and not re.search(r'(?im)^\s+announcementBar: {$', cfg)):
    announcement_bar = announcement_bar.format(indent=indent)
    cfg = re.sub(r'(?i)(?P<indent>\s*)themeConfig: {', r'\g<indent>themeConfig: {\n' + announcement_bar, cfg)
elif (production.lower() == 'true'):
    cfg = re.sub(r'(?ims)\s*announcementBar: {.*?},\n', '\n', cfg)

f = open(manifest, "w")
f.write(cfg)
f.close()
