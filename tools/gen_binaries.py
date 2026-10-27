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
                    + f'  PE32|{name}.efi|*\n\n'
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
            'out by `tools/gen_binaries.py`. Every module keeps its original FFS GUID. Vendor firmware: not\n'
            'for redistribution.\n\n| Module | Type | GUID |\n|---|---|---|\n')
    for n, t, g in drivers:
        f.write(f'| {n} | {t} | {g} |\n')
    f.write('\n| Raw file | GUID |\n|---|---|\n')
    for n, g in raws:
        f.write(f'| {n} | {g} |\n')
json.dump({'drivers': drivers, 'raws': raws}, open(os.path.join(dst, '_index.json'), 'w'), indent=1)
print(f'{len(drivers)} modules, {len(raws)} raw files -> {dst}')
