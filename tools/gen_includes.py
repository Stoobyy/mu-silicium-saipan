#!/usr/bin/env python3
# Make x01aPkg/Include/{APRIORI,DXE,RAW}.inc from bitraPkg's (SM8250, the closest Silicium port)
# by mapping bitra's Qualcomm binaries onto the X01A's own (files/Binaries/x01a/_index.json).
#
#   python -I tools/gen_includes.py <Mu-Silicium>/Platforms/Realme/bitraPkg/Include \
#       files/Binaries/x01a files/Platforms/Balmuda/x01aPkg/Include
import json, os, re, sys

bitra_inc, binaries, out = sys.argv[1:4]
index = json.load(open(os.path.join(binaries, '_index.json')))
ours = {n for n, _, _ in index['drivers']}

# bitra's binary directory -> the X01A module of the same driver (None: the X01A has none).
MAP = {
    'DALSYSDxe': 'DALSys', 'HWIODxe': 'HWIODxeDriver', 'ChipInfoDxe': 'ChipInfo',
    'PlatformInfoDxe': 'PlatformInfoDxeDriver', 'HALIOMMUDxe': 'HALIOMMU', 'SPMIDxe': 'SPMI',
    'TLMMDxe': 'DALTLMM', 'I2CDxe': 'I2C', 'RNGDxe': 'RngDxe',
    'ShmBridgeDxeLA': 'ShmBridgeDxe', 'ScmDxeLA': 'ScmDxe', 'TzDxeLA': 'TzDxe', 'PmicDxeLa': 'PmicDxe',
    'SPIDxe': None, 'SPSSDxe': None, 'OplusProject': None, 'OGaugeAuth': None,
    'XhciPciEmulationDxe': None, 'XhciDxe': None, 'UsbInitDxe': None,
}
BIN = re.compile(r'^(\s*)INF Binaries/bitra/QcomPkg/Drivers/[^/]+/([^/.]+)\.inf\s*$')

def convert(name):
    lines = []
    for line in open(os.path.join(bitra_inc, name)).read().replace('\r', '').split('\n'):
        m = BIN.match(line)
        if m:
            ind, mod = m.groups()
            mod = MAP.get(mod, mod)
            if mod is None:
                continue
            if mod not in ours:
                sys.exit(f'{name}: no X01A module for {m.group(2)}')
            line = f'{ind}INF Binaries/x01a/QcomPkg/Drivers/{mod}/{mod}.inf'
        lines.append(line)
    open(os.path.join(out, name), 'w', newline='\n').write('\n'.join(lines))

os.makedirs(out, exist_ok=True)
convert('APRIORI.inc')
convert('DXE.inc')

# Panels go in only with the Qualcomm display driver; the rest always.
with open(os.path.join(out, 'RAW.inc'), 'w', newline='\n') as f:
    raws = [(n, g) for n, g in index['raws'] if n.endswith(('.xml', '.cfg')) or n == 'BATTERY.PROVISION']
    panels = [r for r in raws if r[0].startswith('Panel_')]
    f.write('!if $(USE_CUSTOM_DISPLAY_DRIVER) == 1\n')
    for n, g in panels:
        f.write(f'  FILE FREEFORM = {g} {{\n    SECTION UI = "{n}"\n    SECTION RAW = Binaries/x01a/RawFiles/{n}\n  }}\n\n')
    f.write('!endif\n\n')
    for n, g in raws:
        if (n, g) not in panels and n != 'uefiplat.cfg':
            f.write(f'  FILE FREEFORM = {g} {{\n    SECTION UI = "{n}"\n    SECTION RAW = Binaries/x01a/RawFiles/{n}\n  }}\n\n')
print('APRIORI.inc DXE.inc RAW.inc ->', out)
