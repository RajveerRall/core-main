#!/usr/bin/env python
__author__ = "Damien Flament"
__contact__ = "damien.flament-sc@airliquide.com"
__copyright__ = "Copyright 2021, Air Liquide"
__date__ = "2021-07-28"
__maintainer__ = "Damien Flament"
__status__ = "Production"
__version__ = "1.4.0"

import json
import yaml
import os
# Module python-frontmatter (not frontmatter)
import frontmatter
import markdown
import io
import argparse

parser = argparse.ArgumentParser(description='Generate json news file')
parser.add_argument("--news-folder", required=True, type=str, help="News folder with md file in it")
parser.add_argument("--url", required=True, type=str, help="URL")
parser.add_argument("--base-url", required=True, type=str, help="Base URL")
parser.add_argument("--config-file", required=True, type=str, help="Landing page configuration file")
parser.add_argument("--destination-file", required=True, type=str, help="Destination json file")
args = parser.parse_args()

news_folder = args.news_folder
url = args.url
base_url = args.base_url.lstrip()
config_file = args.config_file
destination_file = args.destination_file

news_config = yaml.safe_load(open(config_file))['news']
badge_config = yaml.safe_load(open(config_file))['news']['badges']

badges = {}
for badge in badge_config['names']:
    # Create dictionary from config section
    badges[badge['name']] = badge['color']

json_news = {}
news_files = []

# Sort item
for file in os.listdir(news_folder):
    if os.path.isfile(news_folder + '/' + file):
        news_files.append(file)
news_files.sort(reverse=True)

json_news["title"] = "Recent news"
json_news["items"] = []

index = 0
for news_file in news_files:
    print(news_folder + news_file)

    with io.open(news_folder + news_file, 'r') as f:
        news_data = frontmatter.load(f)
        f.close()

    # Find badge color from dictionary
    try:
        badge_color = badges[news_data['badge'].lower()]
    except KeyError:
        badge_color = badge_config['default_color']

    json_news['items'].append({
        "title": news_data['title'],
        "permalink": news_folder + news_file[11:(len(news_file) - 3)],
        "date": news_file[0:10],
        "badge": news_data['badge'],
        "badge_color": badge_color,
        "image": news_data['image'],
        "description": markdown.markdown(news_data.content)[3:-4]
    })
    index = index + 1

    if (index >= news_config['max']):
        # Maximum loadable news on landing page reached
        break

with open(destination_file, 'w') as json_news_file:
    json.dump(json_news, json_news_file)
    json_news_file.close()

# Update image relative url to full url
for news_file in news_files:
    with io.open(news_folder + news_file, 'r') as f:
        news_data = frontmatter.load(f)
        f.close()

        # Update image to image with full url
        if news_data['image'][0:8] != 'https://' and news_data['image'][0:7] != 'http://':
            news_data['image'] = url + base_url + news_data['image']

        for i in range(len(news_data['authors'])):
            if news_data['authors'][i]['image_url'][0:8] != 'https://' and news_data['authors'][i]['image_url'][0:7] != 'http://':
                news_data['authors'][i]['image_url'] = url + base_url + news_data['authors'][i]['image_url']

        with io.open(news_folder + news_file, 'w', encoding='utf8') as updated_news_file:
            updated_news_file.write(frontmatter.dumps(news_data))
            updated_news_file.close()
