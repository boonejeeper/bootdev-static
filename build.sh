#!/bin/bash

# Production build script for the static site generator
# This script builds the site with the correct basepath for GitHub Pages deployment
# The site is built into the docs/ directory for GitHub Pages

echo "Building site for production with basepath: /bootdev-static/"
echo "Output directory: docs/"
python3 src/main.py "/bootdev-static/"
