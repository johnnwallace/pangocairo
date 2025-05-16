import cairocffi as cairo
import pangocffi
import pangocairocffi
from pangocffi import units_to_double, units_from_double

# 1) Parameters
BOX_W, BOX_H = 300, 150            # box size in pixels
MAX_CHARS   = 25                   # hard truncation length
FONT_FAMILY = "Sans"
START_PT    = 36                   # starting (max) point size
MIN_PT      = 8                    # smallest point size to try

def fit_text_to_box(cr, text):
    # truncate
    txt = text if len(text) <= MAX_CHARS else text[:MAX_CHARS+1]
    # make layout
    layout = pangocairocffi.create_layout(cr)
    layout.wrap = pangocffi.WrapMode.WORD_CHAR
    layout.width = units_from_double(BOX_W)
    # try font sizes from START_PT down to MIN_PT
    for pt in range(START_PT, MIN_PT - 1, -1):
        desc = pangocffi.FontDescription()
        desc.family = FONT_FAMILY
        # size in Pango units = points * PANGO_SCALE
        desc.size = units_from_double(pt)
        layout.font_description = desc
        layout.text = txt
        # measure in Pango units
        ink, logical = layout.get_extents()
        w_px = units_to_double(ink.width)
        h_px = units_to_double(ink.height)
        if w_px <= BOX_W and h_px <= BOX_H:
            return layout, w_px, h_px
    # if nothing fits, return at min size
    return layout, w_px, h_px

# 2) Create surface + context
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, BOX_W, BOX_H)
cr = cairo.Context(surface)
cr.set_source_rgb(1,1,1)
cr.paint()

# 3) Fit our text
text = "This is some very long string that we need to truncate & scale"
layout, w_px, h_px = fit_text_to_box(cr, text)

# 4) Center in box
x = (BOX_W - w_px) / 2
y = (BOX_H - h_px) / 2

# 5) Draw & save
cr.move_to(x, y)
cr.set_source_rgb(0, 0, 0)
pangocairocffi.show_layout(cr, layout)
surface.write_to_png("boxed_text.png")
print("Wrote boxed_text.png")
