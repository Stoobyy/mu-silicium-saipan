# mu-silicium-saipan

Mu-Silicium (Project Silicium) support for the Snapdragon 765 / SM7250 ("Saipan", "lito" in Linux).
Upstream has no package for this SoC, so this adds one, plus the first device on it: the BALMUDA Phone
(Kyocera X01A).

Status: boots on the X01A with `fastboot boot`. All drivers load and it reaches the Silicium
boot screen. Nothing to boot into yet.

## What's here

```
files/
  Silicon/Qualcomm/SaipanPkg/     SoC package, based on KonaPkg (SM8250)
  Platforms/Balmuda/x01aPkg/      BALMUDA Phone device package
  Binaries/x01a/                  the phone's own Qualcomm/Kyocera UEFI drivers
  Resources/Configs/x01a.toml     boot image config
  Resources/DTBs/x01a.dtb         Lito v2 base DTB from the stock boot image
tools/
  extract_xbl.py                  unpack the UEFI FV out of an xbl image
  gen_binaries.py                 turn that into Binaries/<device>
  gen_includes.py                 driver lists for the device package, mapped from bitraPkg
apply.sh                          copy all of this into a Mu-Silicium checkout
BASE                              the Mu-Silicium commit this is built against
```

SaipanPkg sets the GIC (0x17A00000 / 0x17A60000), two CPU clusters (6x A55 + 2x A76), SMBIOS
strings, and the display SMMU stream IDs (0xB40-0xB42, 0xF40-0xF42) that get detached in SEC so
the boot splash framebuffer keeps working. There's no DSDT for this SoC yet, so it uses the null ACPI
updater. Kona's updater pokes at fuse registers that may not mean the same thing here.

The X01A memory map and config values come from the phone's own `uefiplat.cfg` (inside xbl), and
the SoC values come from the running phone's device tree. Display is SimpleFb at 1080x1920 on top of
whatever ABL left at 0xA0000000.

## Building

Linux or WSL. Install the packages from Mu-Silicium's `setup_env.sh`, then:

```sh
./apply.sh ~/Mu-Silicium
cd ~/Mu-Silicium
python3 -m venv ~/venv && ~/venv/bin/pip install -r pip-requirements.txt
source ~/venv/bin/activate
python3 build_uefi.py -d x01a -r DEBUG
```

You get `Mu-x01a.img`.

## Testing

Boot it from RAM, don't flash it:

```sh
fastboot boot Mu-x01a.img
```

Rebooting puts you back in Android.

## HakiOS

`hakios/` has the UEFI side of [HakiOS](https://github.com/oosexgang/hackios-xnu-kernel) from its
POCO X5 Pro port: the boot shim copies an "XNUP" payload appended after the FD to 0xF0000000, and
when BDS has nothing to boot it hands over to the XNU loader. Without a payload, the loader only
collects diagnostics (EL, CPU registers, framebuffer, memory map). On the X01A that log is shown on
screen for 60 seconds before it resets, instead of being written to the `logdump` partition.

```sh
./apply.sh --hakios ~/Mu-Silicium
cd ~/Mu-Silicium && python3 build_uefi.py -d x01a -r DEBUG
python3 /path/to/tools/mkxnuimg.py ~/Mu-Silicium [-p payload.bin] -o xnu-x01a.img
fastboot boot xnu-x01a.img
```

HakiOS's own loader (`xnuloader/` in its repo) needs an X01A platform entry, or it takes this phone
for QEMU and pokes QEMU's fw_cfg address. `hakios/xnuloader-x01a.patch` adds it (same GIC and core
numbering as the POCO, framebuffer at 0xA0000000). To build the USB loader image that `xl enter`
would boot:

```sh
tools/build_loader.sh /path/to/hackios-xnu-kernel ~/Mu-Silicium out/xnu-usb.img
fastboot boot out/xnu-usb.img      # then: fastboot getvar product  ->  xnuloader
```

The loader writes its log to the raw `logdump` partition, as on the POCO. On the X01A that
partition is 64 MB and was all zeros; back it up first if yours isn't.

## Adding another SM7250 phone

1. Dump `xbl` from the phone and run `tools/extract_xbl.py` on it.
2. `tools/gen_binaries.py` to lay out `Binaries/<device>`.
3. Copy `x01aPkg`, then fix the memory map, config map and framebuffer size from that phone's
   `uefiplat.cfg` and display panel.
4. Add `Resources/Configs/<device>.toml` and the base DTB from its boot image.

## Notes

- The binaries in `Binaries/x01a` are Qualcomm/Kyocera firmware taken from the phone. They're here
  the same way Project Silicium ships device binaries.
- Code copied or adapted from Mu-Silicium keeps its original license (BSD-2-Clause-Patent).
- This is the UEFI base for running HakiOS on the BALMUDA Phone. That part isn't done yet.
