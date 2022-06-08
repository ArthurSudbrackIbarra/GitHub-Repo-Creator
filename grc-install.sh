#!/bin/bash

# If any error occurs, exits the script.
set -e

# Creates GRC directory.
mkdir GRC
cd GRC
echo "[INFO] Created folder 'GRC', please do not move this folder to another path."

# Clones GRC repository.
git clone https://github.com/ArthurSudbrackIbarra/GitHub-Repo-Creator.git
cd GitHub-Repo-Creator
echo "[INFO] Cloned GRC GitHub repository."

# Giving all users the permission to execute grc script.
chmod +x "$PWD/grc"

# Adding the project directory to $PATH.
sed -i "/grc/d" ~/.bashrc
echo "export PATH+=\":$PWD\" # grc" >> ~/.bashrc
echo "[INFO] Added repository directory to your PATH."

echo "[INFO] You may close this terminal now for the changes to take effect."
