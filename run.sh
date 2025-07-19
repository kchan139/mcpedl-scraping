#!/bin/bash
set -e

if [ "$#" -lt 1 ] || [ "$#" -gt 3 ]; then
    echo "Usage: ./run.sh <category> <category_id> <url>"
    echo "Category: addons, textures, maps"
    echo "Example: ./run.sh addons addon123 https://mcpedl.com/addon-name"
    exit 1
fi

clear
python3 main.py "$@"
