#!/bin/bash

if [ "$#" -lt 1 ] || [ "$#" -gt 3 ]; then
    echo "Usage: ./run.sh <url> [category] [addon_id]"
    echo "Category: addons, textures, maps"
    echo "Example: ./run.sh https://mcpedl.com/addon-name/ addons my_addon_1"
    exit 1
fi

clear
python3 main.py "$@"
