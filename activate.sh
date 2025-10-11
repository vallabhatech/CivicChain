#!/bin/bash

VENV_PATH="./dvoteenv"

if [ -f "$VENV_PATH/bin/activate" ]; then
    source "$VENV_PATH/bin/activate"
    echo "✅ Virtual environment activated."
else
    echo "❌ Could not find activate script at: $VENV_PATH/bin/activate"
    echo "➡️ Did you run: python3 -m venv \"$VENV_PATH\" ?"
    exit 1
fi
