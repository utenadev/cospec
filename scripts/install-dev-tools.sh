#!/bin/bash
set -e

echo "Updating package list and installing dependencies..."
sudo apt-get update
# Install dependencies for comby
sudo apt-get install -y libpcre3-dev libev4
# Install pipx for ast-grep, which is the recommended way to install python CLI tools
sudo apt-get install -y pipx

echo "Installing go-task..."
curl -sL https://taskfile.dev/install.sh | sudo bash -s -- -d -b /usr/local/bin

echo "Installing comby..."
curl -sL get-comby.netlify.app | sudo bash

echo "Installing ast-grep..."
# Use pipx with sudo and custom home/bin directories for a global install.
# Use --force to ensure binaries are re-linked correctly.
sudo PIPX_HOME=/opt/pipx PIPX_BIN_DIR=/usr/local/bin pipx install --force ast-grep-cli

echo "All tools installed successfully."
