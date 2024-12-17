#!/bin/bash

# Check if Marp CLI is installed
if ! command -v marp &> /dev/null; then
    echo "Marp CLI is not installed. Installing..."
    npm install -g @marp-team/marp-cli
fi

# Generate English version
echo "Generating English presentation..."
marp docs/presentation.md --output docs/presentation.pdf --allow-local-files

# Generate Traditional Chinese version
echo "Generating Traditional Chinese presentation..."
marp docs/presentation-zh.md --output docs/presentation-zh.pdf --allow-local-files

echo "Done! Presentations generated in docs/"