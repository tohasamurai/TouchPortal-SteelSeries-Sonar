# -*- coding: utf-8 -*-
"""Generate a simple plugin icon (icon.png)."""
import sys
from PIL import Image, ImageDraw, ImageFont

SIZE = 256
# TP renders category icons at their opaque bounds, so this needs to stay
# deliberately small for the left-side plugin menu.
CONTENT_SIZE = 48
BG = (26, 32, 38, 255)        # dark
ACCENT = (255, 92, 0, 255)    # SteelSeries orange
WHITE = (240, 240, 240, 255)


def rounded(draw, box, r, fill):
    draw.rounded_rectangle(box, radius=r, fill=fill)


def main(out):
    # Draw the original artwork at full resolution first, then scale the whole
    # tile down onto a transparent canvas. This keeps all proportions intact
    # while avoiding an oversized category icon in Touch Portal's menu.
    artwork = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(artwork)
    rounded(d, [8, 8, SIZE - 8, SIZE - 8], 48, BG)

    # speaker cone
    cx, cy = 96, 128
    d.polygon([(60, 104), (96, 104), (140, 72), (140, 184), (96, 152), (60, 152)], fill=WHITE)
    # sound waves (accent arcs)
    for i, r in enumerate((36, 60, 84)):
        d.arc([140 - r + 44, cy - r, 140 + r + 44, cy + r], start=-55, end=55,
              fill=ACCENT, width=10)
    artwork = artwork.resize((CONTENT_SIZE, CONTENT_SIZE), Image.Resampling.LANCZOS)
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    offset = (SIZE - CONTENT_SIZE) // 2
    img.alpha_composite(artwork, (offset, offset))
    img.save(out)
    print("icon written:", out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "icon.png")
