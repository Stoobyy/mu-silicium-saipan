#!/bin/bash
# Put the X01A port (files/ here) into a Mu-Silicium checkout at the commit in BASE.
#   ./apply.sh [--hakios] [MU_SILICIUM_DIR]      (default ~/Mu-Silicium)
# --hakios also applies HakiOS's boot shim payload copy and XNU loader hook (hakios/).
set -e
cd "$(dirname "$(readlink -f "$0")")"
HAKIOS=0
[ "$1" = "--hakios" ] && { HAKIOS=1; shift; }
MU=${1:-$HOME/Mu-Silicium}
[ -d "$MU/.git" ] || { git clone https://github.com/Project-Silicium/Mu-Silicium.git "$MU"; }
git -C "$MU" checkout -q "$(cat BASE)"
git -C "$MU" submodule update --init --recursive
cp -r files/Silicon files/Platforms files/Resources "$MU/"
mkdir -p "$MU/Binaries/x01a" && cp -r files/Binaries/x01a/. "$MU/Binaries/x01a/"
if [ $HAKIOS = 1 ]; then
  PATCH="$PWD/hakios/mu-silicium.patch"
  if git -C "$MU" apply --check --whitespace=nowarn "$PATCH" 2>/dev/null; then
    git -C "$MU" apply --whitespace=nowarn "$PATCH"
  else
    git -C "$MU" apply --check --reverse --whitespace=nowarn "$PATCH"   # already applied
  fi
  cp hakios/XnuLoader.c hakios/XnuLoader.h "$MU/Silicon/Silicium/SiliciumPkg/Library/BootManagerLib/"
fi
echo "apply.sh: done; next: cd $MU && python3 build_uefi.py -d x01a"
