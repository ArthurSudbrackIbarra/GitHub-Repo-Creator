#!/bin/bash

# If any error occurs, exits the script.
set -e

# Purple color for info messages.
PURPLE='\033[0;94m'
NC='\033[0m'

# Check dependencies
# Check pip3
if ! pip3 --version >/dev/null 2>/dev/null; then
  echo -e "${PURPLE}[INFO]${NC} You don't have pip3 installed!"
  exit 1
fi

# If debian, do checks
if awk -F= '/^NAME/{print $2}' /etc/os-release | grep Debian >/dev/null 2>/dev/null; then
  # Check libffi-dev
  APT_LIBFFI_DEV_RES=$(apt-cache search --names-only '^libffi-dev$')
  if [[ $APT_LIBFFI_DEV_RES == "" ]]; then
    echo -e "${PURPLE}[INFO]${NC} You don't have libffi-dev installed!"
    echo -e "${PURPLE}[INFO]${NC} Install with: \"apt install libffi-dev\"!"
    exit 1
  fi
fi

# Creates GRC directory.
mkdir -p GRC
cd GRC
echo -e "${PURPLE}[INFO]${NC} Created folder 'GRC', please do not move this folder to another path."

# Clones GRC repository.
rm -rf GitHub-Repo-Creator
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
