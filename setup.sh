#!/bin/bash

# Giving all users the permission to execute grc.sh script.
chmod +x "$PWD/grc.sh"

# Adding the project directory to $PATH.
NEW_PATH="$PATH:$PWD"
echo "export PATH=\"$NEW_PATH\"" >> ~/.bashrc
source ~/.bashrc
