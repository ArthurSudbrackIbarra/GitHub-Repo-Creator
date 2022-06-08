#!/bin/bash

# Creates hidden directory.
mkdir .grc
cd .grc

# Clones GRC repository.
git clone https://github.com/ArthurSudbrackIbarra/GitHub-Repo-Creator.git

exit 0

# Giving all users the permission to execute grc script.
chmod +x "$PWD/grc"

# Adding the project directory to $PATH.
sed -i "/grc/d" ~/.bashrc
echo "export PATH+=\":$PWD\" # grc" >> ~/.bashrc

echo
echo "You may close this terminal now for the changes to take effect."
echo

# bash <(curl -s http://mywebsite.com/myscript.txt)