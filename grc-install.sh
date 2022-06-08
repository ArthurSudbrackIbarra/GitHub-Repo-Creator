#!/bin/bash

# If any error occurs, exits the script.
set -e

# Purple color for info messages.
PURPLE='\033[0;94m'
NC='\033[0m'

# Creates GRC directory.
mkdir GRC
cd GRC
echo -e "${PURPLE}[INFO]${NC} Created folder 'GRC', please do not move this folder to another path."

# Clones GRC repository.
git clone https://github.com/ArthurSudbrackIbarra/GitHub-Repo-Creator.git
cd GitHub-Repo-Creator
echo -e "${PURPLE}[INFO]${NC} Cloned GRC GitHub repository."

# Giving all users the permission to execute grc script.
chmod +x "$PWD/grc"

# Adding the project directory to $PATH.
sed -i "/grc/d" ~/.bashrc
echo "export PATH+=\":$PWD\" # grc" >> ~/.bashrc
echo -e "${PURPLE}[INFO]${NC} Added repository directory to your PATH."

# Installing python dependencies.
pip3 install -r ./.program-files/requirements.txt
echo -e "${PURPLE}[INFO]${NC} Installed Python dependencies."

echo -e "${PURPLE}[INFO]${NC} You may close this terminal now for the changes to take effect."
