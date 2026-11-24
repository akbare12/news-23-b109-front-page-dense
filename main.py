#!/usr/bin/env python3
"""news-23 b109 front-page-dense: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.

Stdlib only (no PIL). Never writes next to itself: it writes only to MAKEFUN_OUTPUT_DIR,
so it also works from a read-only copy (with MAKEFUN_OUTPUT_DIR pointed elsewhere).
"""
import hashlib
import os
import struct
import sys
import zlib

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
MIN_BYTES = 10_000
MAX_BYTES = 1_048_576


def fail(msg):
    print("error: " + msg, file=sys.stderr)
    return 1


def main():
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not outdir:
        return fail("MAKEFUN_OUTPUT_DIR is empty")
    outdir_abs = os.path.abspath(outdir)
    repo = os.path.dirname(os.path.abspath(__file__))
    if outdir_abs == repo or outdir_abs.startswith(repo + os.sep):
        return fail("MAKEFUN_OUTPUT_DIR must not be inside the repo")
    if os.path.exists(outdir_abs) and not os.path.isdir(outdir_abs):
        return fail("MAKEFUN_OUTPUT_DIR is a file, not a directory")
    if not os.path.exists(SRC):
        return fail("entry.png missing next to main.py")
    with open(SRC, "rb") as f:
        data = f.read()
    if len(data) < MIN_BYTES:
        return fail("entry.png too small: %d bytes" % len(data))
    if len(data) > MAX_BYTES:
        return fail("entry.png too big: %d bytes" % len(data))
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        return fail("not a PNG file")
    # First chunk must be a 13-byte IHDR for a 1024x1024 image.
    # (PNG layout: 8-byte signature, then length(4) + type(4) + data + CRC(4) per chunk.)
    if len(data) < 33:
        return fail("truncated PNG")
    length = struct.unpack(">I", data[8:12])[0]
    ctype = data[12:16]
    if ctype != b"IHDR" or length != 13:
        return fail("first chunk is not a 13-byte IHDR")
    w, h, depth, ctype_id, comp, filt, inter = struct.unpack(">IIBBBBB", data[16:29])
    if (w, h) != (1024, 1024):
        return fail("expected 1024x1024, got %dx%d" % (w, h))
    if depth != 8 or ctype_id not in (2, 6):
        return fail("unexpected bit depth / colour type")
    if comp != 0 or filt != 0 or inter != 0:
        return fail("unexpected compression/filter/interlace")
    ihdr_crc = zlib.crc32(data[12:29]) & 0xFFFFFFFF
    if struct.unpack(">I", data[29:33])[0] != ihdr_crc:
        return fail("IHDR CRC mismatch")
    # Walk chunks: CRC each, every IDAT non-empty, IEND last with no trailing data.
    pos = 8
    idat_total = 0
    last_type = None
    while pos < len(data):
        if pos + 8 > len(data):
            return fail("truncated chunk header")
        clen = struct.unpack(">I", data[pos:pos + 4])[0]
        ctype = data[pos + 4:pos + 8]
        end = pos + 12 + clen
        if end > len(data):
            return fail("truncated chunk %r" % ctype)
        crc = zlib.crc32(data[pos + 4:pos + 8 + clen]) & 0xFFFFFFFF
        if struct.unpack(">I", data[pos + 8 + clen:pos + 12 + clen])[0] != crc:
            return fail("CRC mismatch in chunk %r" % ctype)
        if ctype == b"IDAT":
            if clen == 0:
                return fail("empty IDAT chunk")
            idat_total += clen
        last_type = ctype
        pos = end
    if last_type != b"IEND":
        return fail("last chunk is not IEND")
    if pos != len(data):
        return fail("trailing data after IEND")
    if idat_total < 1000:
        return fail("IDAT payload too small")
    out = os.path.join(outdir_abs, "entry.png")
    if os.path.abspath(out) == os.path.abspath(SRC):
        return fail("refusing to overwrite the source image")
    os.makedirs(outdir_abs, exist_ok=True)
    with open(out, "wb") as f:
        f.write(data)
    with open(out, "rb") as f:
        written = f.read()
    if written != data:
        return fail("re-read mismatch after write")
    print("wrote %s (%d bytes, sha256 %s)" % (out, len(data), hashlib.sha256(data).hexdigest()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
