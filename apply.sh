#!/bin/bash
# Put the X01A port (files/ here) into a Mu-Silicium checkout at the commit in BASE.
#   ./apply.sh [MU_SILICIUM_DIR]      (default ~/Mu-Silicium)
set -e
cd "$(dirname "$(readlink -f "$0")")"
MU=${1:-$HOME/Mu-Silicium}
[ -d "$MU/.git" ] || { git clone https://github.com/Project-Silicium/Mu-Silicium.git "$MU"; }
git -C "$MU" checkout -q "$(cat BASE)"
git -C "$MU" submodule update --init --recursive
cp -r files/Silicon files/Platforms files/Resources "$MU/"
mkdir -p "$MU/Binaries/x01a" && cp -r files/Binaries/x01a/. "$MU/Binaries/x01a/"
echo "apply.sh: done; next: cd $MU && python3 build_uefi.py -d x01a"
