import cairocffi as cairo
import pangocffi
import pangocairocffi
from pangocffi import units_to_double, units_from_double

IMG_WIDTH = 1080
IMG_HEIGHT = 1920
CONTENT_WIDTH = 780
TITLE_OFFSET = 100
TITLE_HEIGHT = 200

FONT_FAMILY = "sans"
TITLE_LIM = 25

# Create canvas
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, IMG_WIDTH, IMG_HEIGHT)
cr = cairo.Context(surface)
cr.set_source_rgb(1,1,1)
cr.paint()

# Playlist title layout
TITLE = "WWWWWW"
layout = pangocairocffi.create_layout(cr)
layout.wrap = pangocffi.WrapMode.WORD_CHAR
layout.width = units_from_double(CONTENT_WIDTH)
title = TITLE if len(TITLE) <= 25 else TITLE[:TITLE_LIM]

# decrease font size until it fits
for pt in range(100, 0 - 1, -1):
    desc = pangocffi.FontDescription()
    desc.family = FONT_FAMILY
    desc.size = units_from_double(pt)
    layout.font_description = desc
    layout.text = title
    layout.alignment = pangocffi.Alignment(1)
    # measure in Pango units
    ink, logical = layout.get_extents()
    w_px = units_to_double(ink.width)
    h_px = units_to_double(ink.height)
    if h_px <= TITLE_HEIGHT:
        break

print(pt)

# 5) Draw & save
cr.move_to((IMG_WIDTH - CONTENT_WIDTH) / 2, TITLE_OFFSET)
cr.set_source_rgb(0, 0, 0)
pangocairocffi.show_layout(cr, layout)
surface.write_to_png("shareable.png")