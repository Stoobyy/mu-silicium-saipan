#!/usr/bin/env python3
# Unpack the UEFI firmware volume inside a Qualcomm xbl image into one file per section.
#   python -I tools/extract_xbl.py xbl_a.img OUT_DIR
import gzip, sys, struct, lzma, uuid, os, json
LZMA = uuid.UUID('EE4E5898-3914-4259-9D6E-DC7BD79403CF')
TYPES = {1:'RAW',2:'FREEFORM',3:'SEC',4:'PEICORE',5:'DXECORE',6:'PEIM',7:'DRIVER',9:'APP',0xb:'FVIMAGE',0xf0:'PAD'}
out = sys.argv[2]; os.makedirs(out, exist_ok=True)
files = []
def a8(x): return (x+7)&~7
def a4(x): return (x+3)&~3
def sections(buf, ctx):
    p = 0
    while p + 4 <= len(buf):
        sz = int.from_bytes(buf[p:p+3],'little'); t = buf[p+3]; h = 4
        if sz == 0xffffff: sz = struct.unpack_from('<I', buf, p+4)[0]; h = 8
        if sz < h: break
        body = buf[p+h:p+sz]
        if t == 0x02:  # GUID defined
            g = uuid.UUID(bytes_le=bytes(body[:16])); off = struct.unpack_from('<H', body, 16)[0]
            data = buf[p+off:p+sz]
            if g == LZMA:
                sections(lzma.decompress(bytes(data), format=lzma.FORMAT_ALONE), ctx)
            elif bytes(data[:2]) == b'\x1f\x8b':
                sections(gzip.decompress(bytes(data)), ctx)
            else: ctx.setdefault('unk',[]).append(str(g))
        elif t == 0x01: sections(lzma.decompress(bytes(body[5:]), format=lzma.FORMAT_ALONE) if body[4]==2 else body[5:], ctx)
        elif t == 0x17: fv(body, ctx.get('depth',0)+1)
        elif t == 0x15: ctx['name'] = bytes(body).decode('utf-16-le').rstrip('\0')
        elif t in (0x10, 0x11, 0x12, 0x13, 0x14, 0x19): ctx.setdefault('secs',[]).append((t, bytes(body)))
        p = a4(p + sz)
def fv(buf, depth=0):
    hl = struct.unpack_from('<H', buf, 0x30)[0]; fvlen = struct.unpack_from('<Q', buf, 0x20)[0]
    p = hl
    while p + 24 <= min(len(buf), fvlen):
        g = uuid.UUID(bytes_le=bytes(buf[p:p+16]))
        if buf[p:p+24] == b'\xff'*24: break
        t = buf[p+0x12]; attr = buf[p+0x13]; sz = int.from_bytes(buf[p+0x14:p+0x17],'little'); h = 24
        if attr & 1: sz = struct.unpack_from('<Q', buf, p+24)[0]; h = 32
        if sz < h: break
        ctx = {'depth': depth}
        if t not in (0xf0, 1):
            try: sections(buf[p+h:p+sz], ctx)
            except Exception as e: ctx['err'] = repr(e)
        if t != 0xf0:
            name = ctx.get('name', str(g))
            files.append((depth, TYPES.get(t, hex(t)), name, str(g), sz, ctx.get('err'), [st for st, _ in ctx.get('secs', [])], 'name' in ctx))
            for st, b in ctx.get('secs', []):
                ext = {0x10:'efi',0x11:'pic',0x12:'te',0x13:'depex',0x14:'ver',0x19:'raw'}[st]
                if st in (0x10,0x12,0x13,0x19):
                    open(os.path.join(out, f"{name}.{ext}"), 'wb').write(b)
        p = a8(p + sz)
d = open(sys.argv[1],'rb').read()
# the UEFI FD is the ELF segment that holds a firmware volume header
base = d.find(b'_FVH') - 0x28
fv(d[base:base + struct.unpack_from('<Q', d, base + 0x20)[0]])
for f in files: print(('  '*f[0]) + f"{f[1]:9s} {f[2]:34s} {f[4]:#9x}" + (f"  ERR {f[5]}" if f[5] else ''))
print("total files", len(files))
json.dump([{'depth': f[0], 'type': f[1], 'name': f[2], 'guid': f[3].upper(), 'secs': f[6], 'has_ui': f[7]} for f in files],
          open(os.path.join(out, '_manifest.json'), 'w'), indent=1)
