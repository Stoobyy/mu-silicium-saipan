#!/usr/bin/env python3
# Lay the X01A's own UEFI drivers (extracted from xbl_a.img by tools/extract_xbl.py) out
# as Mu-Silicium binary modules: files/Binaries/x01a/QcomPkg/Drivers/<Name>/<Name>.{inf,efi,depex}
# and files/Binaries/x01a/RawFiles/<file>, every module keeping its original FFS GUID.
#
#   python -I tools/gen_binaries.py XBL_OUT_DIR files/Binaries/x01a
import json, os, shutil, struct, sys

src, dst = sys.argv[1], sys.argv[2]
manifest = json.load(open(os.path.join(src, '_manifest.json')))

# Modules Mu-Silicium builds from source instead (see Include/*.inc), and the Qualcomm SEC/FV.
FROM_SOURCE = {
    'DxeCore', 'RuntimeDxe', 'ArmCpuDxe', 'ArmGicDxe', 'MetronomeDxe', 'ArmTimerDxe', 'DiskIoDxe',
    'PartitionDxe', 'EnglishDxe', 'FvSimpleFileSystem', 'Fat', 'VariableDxe', 'WatchdogTimer',
    'EmbeddedMonotonicCounter', 'RealTimeClock', 'PrintDxe', 'DevicePathDxe', 'CapsuleRuntimeDxe',
    'HiiDatabase', 'SimpleTextInOutSerial', 'ConPlatformDxe', 'ConSplitterDxe', 'GraphicsConsoleDxe',
    'SecurityStubDxe',
}

# Byte patches, the same ones Silicium applies to these drivers on SM8250 (bitra), found at the
# same code in the Saipan builds: (file offset, original bytes, new bytes).
PATCHES = {
    # The TZ applets were already loaded by the stock UEFI before ABL; loading them again fails
    # with Device Error and TzDxe asserts. Set the "applets loaded" flag to TRUE. (N1kroks)
    'TzDxe': [(0xD469, b'\x00', b'\x01')],
    # DisplayFeatureEnablerInit turns the display clocks on again, which drops the framebuffer
    # ABL left running. Make it return EFI_SUCCESS. (N1kroks)
    'FeatureEnablerDxe': [(0x1790, bytes.fromhex('ffc300d1f30b00f9'), bytes.fromhex('e0031f2ac0035fd6'))],
}

# PE subsystem -> INF MODULE_TYPE. Runtime drivers too are DXE_DRIVER, as in Silicium's other
# Binaries: Common.fdf.inc has no DXE_RUNTIME_DRIVER.BINARY rule, and the FFS type is the same.
SUBSYSTEM = {10: 'UEFI_APPLICATION', 11: 'DXE_DRIVER', 12: 'DXE_DRIVER'}

def pe_subsystem(path):
    d = open(path, 'rb').read(0x2000)
    pe = struct.unpack_from('<I', d, 0x3c)[0]
    return struct.unpack_from('<H', d, pe + 0x18 + 0x44)[0]

shutil.rmtree(dst, ignore_errors=True)
drivers, raws = [], []
for e in manifest:
    name, guid = e['name'], e['guid']
    if e['type'] in ('DRIVER', 'APP') and name not in FROM_SOURCE:
        efi = os.path.join(src, name + '.efi')
        depex = os.path.join(src, name + '.depex')
        kind = 'Application' if e['type'] == 'APP' else 'Drivers'
        out = os.path.join(dst, 'QcomPkg', kind, name)
        os.makedirs(out)
        shutil.copy(efi, out)
        has_depex = os.path.exists(depex)
        if has_depex:
            shutil.copy(depex, out)
        mtype = SUBSYSTEM[pe_subsystem(efi)]
        pe32 = name + '.efi'
        if name in PATCHES:
            d = bytearray(open(efi, 'rb').read())
            for off, old, new in PATCHES[name]:
                if d[off:off + len(old)] != old:
                    sys.exit(f'{name}: unexpected bytes at {off:#x}, not patching')
                d[off:off + len(new)] = new
            pe32 = name + '.patched.efi'
            open(os.path.join(out, pe32), 'wb').write(d)
        with open(os.path.join(out, name + '.inf'), 'w', newline='\n') as f:
            f.write('[Defines]\n'
                    '  INF_VERSION                    = 0x0001001B\n'
                    f'  BASE_NAME                      = {name}\n'
                    f'  FILE_GUID                      = {guid}\n'
                    f'  MODULE_TYPE                    = {mtype}\n'
                    '  VERSION_STRING                 = 1.0\n'
                    '  ENTRY_POINT                    = EfiEntry\n\n'
                    '[Binaries.AARCH64]\n'
                    + (f'  DXE_DEPEX|{name}.depex|*\n' if has_depex else '')
                    + f'  PE32|{pe32}|*\n\n'
                    '[Depex]\n  TRUE\n')
        drivers.append((name, mtype, guid))
    elif e['type'] == 'FREEFORM' and e['has_ui']:
        os.makedirs(os.path.join(dst, 'RawFiles'), exist_ok=True)
        shutil.copy(os.path.join(src, name + '.raw'), os.path.join(dst, 'RawFiles', name))
        raws.append((name, guid))

with open(os.path.join(dst, 'README.md'), 'w', newline='\n') as f:
    f.write('# Balmuda Phone X01A UEFI binaries\n\n'
            'Extracted from the phone\'s own `xbl_a.img` (BOOT.XF.3.3.1-00060-SAIPANLAZ-1, ELF segment 11 =\n'
            'the UEFI FD at 0x9FC00000; inner FV gzip, GUID 1D301FE9-BE79-4353-91C2-D23BC959AE0C) and laid\n'
            'out by `tools/gen_binaries.py`. Every module keeps its original FFS GUID. This is Qualcomm and\n'
            'Kyocera firmware, shipped here the same way Project Silicium ships device binaries.\n\n'
            '## Patches\n\n'
            '### TzDxe\n\n'
            '- Reason: the stock UEFI already loaded the TZ applets before ABL. Loading them again fails with\n'
            '  Device Error and TzDxe asserts.\n'
            '- Patch: the "applets loaded" flag (0xD469) starts as TRUE.\n'
            '- Patch creator: [N1kroks](https://github.com/N1kroks/) (same patch as the SM8250 binaries)\n\n'
            '### FeatureEnablerDxe\n\n'
            '- Reason: DisplayFeatureEnablerInit turns the display clocks on again and the framebuffer is lost.\n'
            '- Patch: the function (0x1790) returns EFI_SUCCESS right away.\n'
            '- Patch creator: [N1kroks](https://github.com/N1kroks/) (same patch as the SM8250 binaries)\n\n'
            '## Modules\n\n| Module | Type | GUID |\n|---|---|---|\n')
    for n, t, g in drivers:
        f.write(f'| {n} | {t} | {g} |\n')
    f.write('\n| Raw file | GUID |\n|---|---|\n')
    for n, g in raws:
        f.write(f'| {n} | {g} |\n')
json.dump({'drivers': drivers, 'raws': raws}, open(os.path.join(dst, '_index.json'), 'w', newline='\n'), indent=1)
print(f'{len(drivers)} modules, {len(raws)} raw files -> {dst}')
