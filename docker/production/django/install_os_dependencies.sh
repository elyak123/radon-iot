#!/bin/bash

# Bash "strict mode", to help catch problems and bugs in the shell
# script. Every bash script you write should include this. See
# http://redsymbol.net/articles/unofficial-bash-strict-mode/ for
# details.
set -euo pipefail

# Tell apt-get we're never going to be able to give manual
# feedback:
export DEBIAN_FRONTEND=noninteractive

# Update the package listing, so we know what package exist:
apt-get update > /dev/null

# Install security updates:
apt-get -y upgrade > /dev/null

# Install a new package, without unnecessary recommended packages:
apt-get -y install --no-install-recommends libpq-dev git gcc libc-dev binutils libproj-dev gdal-bin > /dev/null

# Delete cached files we don't need anymore:
apt-get clean

rm -rf /var/lib/apt/lists/*
