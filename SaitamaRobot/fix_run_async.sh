#!/bin/bash

# Remove all lines that contain only @run_async (with optional spaces/tabs)
find . -type f -name "*.py" -exec sed -i '/^\s*@run_async\s*$/d' {} +

# Add run_async=True param to handler constructors, if not already present
# This handles CommandHandler, MessageHandler, RegexHandler, and CustomCommandHandler

find . -type f -name "*.py" | while read -r file; do
    # Only add run_async if not already present on that line
    sed -i -r '/(CommandHandler|MessageHandler|RegexHandler|CustomCommandHandler)\(/ {
        /run_async\s*=/! s/(\(([^)]*))/\1, run_async=True/'
    }' "$file"
done
