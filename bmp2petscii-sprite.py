from PIL import Image, ImageOps
import sys

# 2x2 bitmap pattern to PETSCII
# bits:
# 1 = top-left
# 2 = top-right
# 4 = bottom-left
# 8 = bottom-right
LUT = [
    32,   # 0  empty
    126,  # 1  tl
    124,  # 2  tr
    226,  # 3  top half
    123,  # 4  bl
    97,   # 5  left half
    255,  # 6  tr+bl
    236,  # 7  all but br
    108,  # 8  br
    127,  # 9  tl+br
    225,  # 10 right half
    251,  # 11 all but bl
    98,   # 12 bottom half
    252,  # 13 all but tr
    254,  # 14 all but tl
    160   # 15 full block
]


# 9 shifts: centre + 8 directions
SHIFTS = [
    ("C",  0,  0),
    ("N",  0, -1),
    ("NE", 1, -1),
    ("E",  1,  0),
    ("SE", 1,  1),
    ("S",  0,  1),
    ("SW",-1,  1),
    ("W", -1,  0),
    ("NW",-1, -1),
]

TRANSPARENT = 0   # use 32 instead if you want space
PAD = 1           # padding allows 1-pixel shifts without clipping

def bit(v):
    return 1 if v else 0

def load_image(path, invert=False, dither=False):
    im = Image.open(path)

    if invert:
        # invert safely via L mode
        im = ImageOps.invert(im.convert("L"))
    else:
        im = im.convert("L")

    if dither:
        im = im.convert("1")
    else:
        im = im.convert("1", dither=Image.NONE)

    return im

def pad_image(im, pad=1):
    w, h = im.size
    out = Image.new("1", (w + pad * 2, h + pad * 2), 0)
    out.paste(im, (pad, pad))
    return out

def shift_image(im, dx, dy):
    """Shift the view by (dx, dy): out[x,y] = im[x+dx, y+dy]. Paste at (-dx,-dy)."""
    w, h = im.size
    out = Image.new("1", (w, h), 0)
    out.paste(im, (-dx, -dy))
    return out

def image_to_petscii(im, transparent=0):
    w, h = im.size
    px = im.load()


    padded = Image.new("1", (w + 2, h + 2), 0)
    padded.paste(im, (0, 0))
    im = padded
    px = im.load()
    w, h = im.size

    rows = []
    flat = []

    for y in range(0, h, 2):
        row = []
        for x in range(0, w, 2):
            tl = bit(px[x, y])
            tr = bit(px[x + 1, y])
            bl = bit(px[x, y + 1])
            br = bit(px[x + 1, y + 1])

            idx = tl | (tr << 1) | (bl << 2) | (br << 3)

            if idx == 0:
                ch = transparent
            else:
                ch = LUT[idx]

            row.append(ch)
            flat.append(ch)

        rows.append(row)

    return rows, flat, w // 2, h // 2

def emit_block(label, rows, flat, cw, ch):
    print(f"{label}_W = {cw}")
    print(f"{label}_H = {ch}")
    print(f"{label}:")
    print("DATA AS BYTE _")
    for r, row in enumerate(rows):
        line = ",".join(str(v) for v in row)
        if r < len(rows) - 1:
            print(line + ", _")
        else:
            print(line)
    print()

def main():
    if len(sys.argv) < 2:
        print("Need filename")
        sys.exit(1)

    filename = sys.argv[1]
    invert = "-invert" in sys.argv
    dither = "-dither" in sys.argv
    transparent = 32 #if "-space" in sys.argv else TRANSPARENT

    im = load_image(filename, invert=invert, dither=dither)
    w, h = im.size

    print(f"REM source image: {w}x{h} pixels")

    # pad so shifts do not crop the object
    padded = pad_image(im, PAD)
    pw, ph = padded.size
    print(f"REM padded image: {pw}x{ph} pixels")
    print()

    for name, dx, dy in SHIFTS:
        # because we padded by 1, shifting is just pasting with offset
        shifted = shift_image(padded, dx, dy)
        rows, flat, cw, ch = image_to_petscii(shifted, transparent=transparent)
        emit_block(name, rows, flat, cw, ch)

if __name__ == "__main__":
    main()