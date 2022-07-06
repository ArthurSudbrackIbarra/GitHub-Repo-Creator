#!/bin/bash

# If any error occurs, exits the script.
set -e

# Terminal colors.
RED='\033[31m'
GREEN='\033[32m'
PURPLE='\033[0;94m'
NC='\033[0m'

# Checking dependencies.

# Checking pip3.
if ! pip3 --version >/dev/null 2>/dev/null; then
  echo -e "${RED}[ERROR]${NC} You don't have pip3 installed!"
  exit 1
fi

# If OS is Debian, do some checks.
if [[ -f /etc/os-release ]]; then
  if awk -F= '/^NAME/{print $2}' /etc/os-release | grep Debian >/dev/null 2>/dev/null; then
    # Checking libffi-dev.
    APT_LIBFFI_DEV_RES=$(apt-cache search --names-only '^libffi-dev$')
    if [[ $APT_LIBFFI_DEV_RES == "" ]]; then
      echo -e "${RED}[ERROR]${NC} You don't have libffi-dev installed! Install with: \"apt install libffi-dev\"."
      exit 1
    fi
  fi
fi

# Creates GRC directory in /opt.
mkdir -p /opt/grc
cd /opt/grc
echo -e "${PURPLE}[INFO]${NC} Created directory grc in /opt."

# Clones GRC repository.
rm -rf GitHub-Repo-Creator
git clone https://github.com/ArthurSudbrackIbarra/GitHub-Repo-Creator.git --quiet > /dev/null
cd GitHub-Repo-Creator
# git checkout v3.0.3 --quiet > /dev/null
git checkout improve-unix-installation-process --quiet > /dev/null
echo -e "${PURPLE}[INFO]${NC} Cloned GRC GitHub repository."

# Giving all users the permission to execute grc script.
chmod +x grc

# Giving permissions to read and write to folders.
chmod ugo+rw .program-files/configurations
chmod ugo+rw templates
chmod ugo+rw repositories

# Moving grc executable to /usr/bin.
mv -f grc /usr/bin
echo -e "${PURPLE}[INFO]${NC} Moved grc executable to /usr/bin."

# Installing python dependencies.
pip3 install -r ./.program-files/requirements.txt > /dev/null
echo -e "${PURPLE}[INFO]${NC} Installed Python dependencies."

echo
echo "   _____   _____     _____ "
echo "  / ____| |  __ \   / ____|"
echo " | |  __  | |__) | | |     "
echo " | | |_ | |  _  /  | |     "
echo " | |__| | | | \ \  | |____ "
echo "  \_____| |_|  \_\  \_____|"
echo
echo

echo
echo -e "${GREEN}[SUCCESS]${NC} GRC was successfully installed!"
echo
