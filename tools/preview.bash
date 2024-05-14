#!/usr/bin/env bash

# Only for local preview, not for production

# TODO: write a python script to monitor and reflect changes in docusaurus preview
# TODO: explain folder structure
# TODO: update submodules


cd "../tech-guides/" || exit 1
yarn start
cd "../tools/" || exit 1
