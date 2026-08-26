# -*- coding: utf-8 -*-
"""Generate compact, transparent Touch Portal button icons."""
from pathlib import Path
from PIL import Image, ImageDraw

SIZE = 256
OUTLINE = (22, 29, 34, 255)
DARK = (50, 67, 74, 255)
TEAL = (78, 123, 129, 255)
BLUE = (42, 157, 221, 255)
LIGHT = (181, 229, 246, 255)


def image():
    return Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))


def headset(path):
    im = image(); d = ImageDraw.Draw(im)
    # Headband and cyan inner edge
    d.arc((62, 42, 194, 183), 188, 352, fill=OUTLINE, width=15)
    d.arc((68, 48, 188, 177), 190, 350, fill=TEAL, width=5)
    # Earcups
    for box in ((51, 129, 88, 186), (168, 129, 205, 186)):
        d.rounded_rectangle(box, radius=12, fill=OUTLINE)
        inner = (box[0]+6, box[1]+6, box[2]-6, box[3]-6)
        d.rounded_rectangle(inner, radius=8, fill=TEAL)
    # Boom mic, clear and compact
    d.line((188, 174, 182, 201, 151, 214), fill=OUTLINE, width=10)
    d.line((188, 174, 182, 201, 151, 214), fill=BLUE, width=4)
    d.rounded_rectangle((132, 207, 155, 220), radius=6, fill=OUTLINE)
    d.rounded_rectangle((137, 210, 152, 217), radius=3, fill=BLUE)
    im.save(path)


def studio(path):
    im = image(); d = ImageDraw.Draw(im)
    # Capsule and grille
    d.rounded_rectangle((82, 38, 174, 154), radius=40, fill=OUTLINE)
    d.rounded_rectangle((90, 46, 166, 146), radius=32, fill=DARK)
    for y in range(60, 113, 13):
        d.line((104, y, 152, y), fill=TEAL, width=4)
    # Yoke around capsule
    d.arc((63, 91, 193, 192), 8, 172, fill=OUTLINE, width=11)
    d.arc((63, 91, 193, 192), 8, 172, fill=BLUE, width=4)
    # Stem and desk base
    d.rounded_rectangle((119, 169, 137, 203), radius=6, fill=OUTLINE)
    d.rounded_rectangle((123, 173, 133, 199), radius=4, fill=BLUE)
    d.ellipse((79, 194, 177, 220), fill=OUTLINE)
    d.ellipse((86, 199, 170, 215), fill=DARK)
    d.arc((86, 199, 170, 215), 10, 170, fill=BLUE, width=3)
    # Small blue status LED
    d.ellipse((121, 125, 137, 141), fill=BLUE)
    d.ellipse((125, 129, 133, 137), fill=LIGHT)
    im.save(path)


if __name__ == "__main__":
    target = Path(__file__).resolve().parent.parent / "assets"
    target.mkdir(exist_ok=True)
    headset(target / "headset_microphone.png")
    studio(target / "studio_microphone.png")
