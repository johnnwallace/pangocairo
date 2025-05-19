import cairocffi as cairo
import pangocffi
import pangocairocffi
from pangocffi import units_to_double, units_from_double
import qrcode
from PIL import Image
import os

def auto_size(text, height, layout):
    for pt in range(1000, -1, -1):
        desc = pangocffi.FontDescription()
        desc.family = FONT_FAMILY
        desc.size = units_from_double(pt)
        layout.font_description = desc
        layout.text = text
        layout.alignment = pangocffi.Alignment(1)
        ink, _ = layout.get_extents()
        h_px = units_to_double(ink.height)
        if h_px <= height:
            return True
    return False


IMG_WIDTH = 1080
IMG_HEIGHT = 1920
CONTENT_WIDTH = 780
TITLE_OFFSET = 100
TITLE_HEIGHT = 200
CAPTION_HEIGHT = 100
LOGO_HEIGHT = 100
LOGO_WIDTH = 365

OFFSET = 50

FONT_FAMILY = "sans"
TITLE_LIM = 25
USER_LIM = 18

# Create canvas
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, IMG_WIDTH, IMG_HEIGHT)
cr = cairo.Context(surface)
cr.set_source_rgb(1,1,1)
cr.paint()

# PLAYLIST TITLE ===============================================================
TITLE = "WWWWWWWWWWWWWWWWWWWW"
layout = pangocairocffi.create_layout(cr)
layout.wrap = pangocffi.WrapMode.WORD_CHAR
layout.width = units_from_double(CONTENT_WIDTH)
title = TITLE if len(TITLE) <= TITLE_LIM else TITLE[:TITLE_LIM]

# decrease font size until it fits
if auto_size(title, TITLE_HEIGHT, layout):
    cr.move_to((IMG_WIDTH - CONTENT_WIDTH) / 2, TITLE_OFFSET)
    cr.set_source_rgb(0, 0, 0)
    pangocairocffi.show_layout(cr, layout)
else:
    print("Title too long")
    exit()

# CAPTION ======================================================================
USERNAME = "Lego2222"
layout = pangocairocffi.create_layout(cr)
layout.wrap = pangocffi.WrapMode.WORD_CHAR
layout.width = units_from_double(CONTENT_WIDTH)
username = USERNAME if len(USERNAME) <= USER_LIM else USERNAME[:USER_LIM]

# decrease font size until it fits
if auto_size(f"by {username} on palify.me", CAPTION_HEIGHT, layout):
    caption_y = TITLE_OFFSET + TITLE_HEIGHT + 2 * OFFSET + CONTENT_WIDTH
    caption_x = (IMG_WIDTH - CONTENT_WIDTH) / 2
    cr.move_to(caption_x, caption_y)
    cr.set_source_rgb(0, 0, 0)
    pangocairocffi.show_layout(cr, layout)
else:
    print("Caption too long")
    exit()

surface.write_to_png("temp_text.png")

# Combine all images using PIL
text_img = Image.open("temp_text.png")

# AVATAR =======================================================================
avatar_size = CONTENT_WIDTH  # Make avatar same width as content
avatar = Image.open("avatar.png")
avatar = avatar.resize((avatar_size, avatar_size))

# Calculate avatar position (centered horizontally, below title)
avatar_x = (IMG_WIDTH - avatar_size) // 2
avatar_y = TITLE_OFFSET + TITLE_HEIGHT + OFFSET

# LOGO ========================================================================
logo = Image.open("logo.png").convert("RGBA")
logo = logo.resize((LOGO_WIDTH, LOGO_HEIGHT))

logo_x = (IMG_WIDTH - LOGO_WIDTH) // 2
logo_y = IMG_HEIGHT - LOGO_HEIGHT - OFFSET

# QR CODE ======================================================================
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=20,  # Reduced box size for better proportions
    border=0,
)
qr.add_data("https://www.palify.me/")
qr.make(fit=True)

qr_img = qr.make_image(fill_color="black", back_color="white")

# Define QR code size and position
qr_size = logo_y - caption_y - CAPTION_HEIGHT - 2 * OFFSET # Define QR code size
qr_img = qr_img.resize((qr_size, qr_size))

# Calculate position for QR code (centered horizontally, below the avatar and caption)
qr_x = (IMG_WIDTH - qr_size) // 2
qr_y = caption_y + CAPTION_HEIGHT + OFFSET

# Convert RGBA to RGB if needed
if text_img.mode == 'RGBA':
    text_img = text_img.convert('RGB')

# Paste avatar, QR code, and logo onto main image
text_img.paste(avatar, (avatar_x, avatar_y))
text_img.paste(qr_img, (qr_x, qr_y))
text_img.paste(logo, (logo_x, logo_y), logo)

# Save final combined image
text_img.save("shareable.png")

# Clean up temporary file
os.remove("temp_text.png")