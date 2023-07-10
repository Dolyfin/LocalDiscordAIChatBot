#!/bin/bash

VENV_DIR=venv

if [ ! -d "$VENV_DIR" ]; then
    echo "<!> Creating virtual environment..."
    python3 -m venv $VENV_DIR
fi

echo "<!> Activating virtual environment..."
source $VENV_DIR/bin/activate

echo "<!> Installing required packages..."
pip install -r requirements.txt

echo "<!> Starting the bot..."
python main.py

read -p "Press Enter to exit..."