#!/bin/bash

# Build script for production deployment to GitHub Pages
echo "Building site for production with basepath /static-site-generator/"
python3 src/main.py "/static-site-generator/"
echo "Build complete! Site built to docs/ directory"