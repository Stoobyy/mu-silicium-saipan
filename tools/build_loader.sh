#!/bin/bash
# Build HakiOS's XNU loader with the X01A platform (hakios/xnuloader-x01a.patch) and pack it as a
# USB payload image, the way `xl enter` does on the POCO.
#   tools/build_loader.sh HAKIOS_DIR MU_SILICIUM_DIR [OUT_IMG]
# The identity header is the placeholder one (no Apple data) unless HAKIOS_DIR/xnuloader/identity.h
# already exists.
set -e
HERE=$(cd "$(dirname "$0")/.." && pwd)
HAKIOS=$1; MU=$2; OUT=${3:-$HERE/out/xnu-usb.img}
W=$(mktemp -d); trap 'rm -rf "$W"' EXIT
cp -r "$HAKIOS/xnuloader" "$HAKIOS/sysimage" "$W/"
cd "$W/xnuloader"
sed -i 's/\r$//' *.c *.h *.sh *.py
patch -p1 < "$HERE/hakios/xnuloader-x01a.patch"
[ -f identity.h ] || bash mkidentity.sh --placeholder
clang --target=aarch64-unknown-windows -ffreestanding -fno-builtin -fno-stack-protector -fshort-wchar \
  -mgeneral-regs-only -O1 -Wall -Wextra -Wno-unused-parameter -c loader.c -o loader.obj
# 0xA8000000: free DDR on the X01A (HakiOS's 0xA1000000 is inside this phone's framebuffer region)
lld-link /subsystem:efi_application /entry:efi_main /nodefaultlib /base:0xA8000000 /out:loader.efi loader.obj
python3 mkpayload.py -o usb-payload.bin loader.efi=loader.efi --usb
python3 "$HERE/tools/mkxnuimg.py" "$MU" -p usb-payload.bin -o "$OUT"
