#!/bin/bash

# Giving all users the permission to execute grc.sh script.
chmod +x "$PWD/grc"

# Adding the project directory to $PATH.
sed -i "/grc_project/d" ~/.bashrc
echo "export PATH+=\":$PWD\" # grc_project" >> ~/.bashrc

echo
echo "You may close this terminal now for the changes to take effect."
echo
