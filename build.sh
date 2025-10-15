#!/bin/bash
# Extract repo name from git remote URL
REPO_NAME=$(git remote get-url origin | sed 's/.*\/\([^/]*\)\.git$/\1/')
python3 src/main.py "/$REPO_NAME/"
