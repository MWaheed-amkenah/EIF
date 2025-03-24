from PIL import Image, ImageDraw, ImageFont, ImageSequence
import arabic_reshaper
from bidi.algorithm import get_display
import io
import os

def contains_arabic(text):
    return any('\u0600' <= c <= '\u06FF' or '\u0750' <= c <= '\u077F' for c in text)

def reshape_arabic_text(text):
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)

def add_name_to_gif(input_gif_path, name_text, eng_font_path="29lt-bukra.ttf", ar_font_path="29lt-bukra-bold.ttf", font_size=24):
    gif = Image.open(input_gif_path)
    frames = []
    duration = gif.info.get('duration', 100)

    # Ensure Arabic text is reshaped
    if contains_arabic(name_text):
        name_text = reshape_arabic_text(name_text)
        font_path = ar_font_path
    else:
        font_path = eng_font_path

    # Check if the font file exists
    if not os.path.exists(font_path):
        print(f"⚠️ Font {font_path} not found! Using default font.")
        font = ImageFont.load_default()
    else:
        font = ImageFont.truetype(font_path, font_size)

    try:
        while True:
            frame = gif.copy().convert("RGBA")
            draw = ImageDraw.Draw(frame)

            width, height = frame.size
            bbox = draw.textbbox((0, 0), name_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            # Correct placement: ~320px from the bottom as per your HTML preview
            position_x = (width - text_width) / 2
            position_y = height - 321 - text_height / 2

            # Add subtle shadow for visibility
            draw.text((position_x + 2, position_y + 2), name_text, font=font, fill=(0, 0, 0, 150))

            # Draw bold-like effect by multiple passes
            bold_offsets = [(0,0), (1,0), (0,1), (1,1)]
            for offset in bold_offsets:
                draw.text((position_x + offset[0], position_y + offset[1]), name_text, font=font, fill="black")

            frames.append(frame.convert("P"))
            gif.seek(gif.tell() + 1)
    except EOFError:
        pass

    # Save as in-memory or output file
    output_gif = io.BytesIO()
    frames[0].save(
        output_gif,
        format='GIF',
        save_all=True,
        append_images=frames[1:],
        duration=duration,
        loop=0
    )
    output_gif.seek(0)
    return output_gif

# ✅ Example usage:
with open("EIF-personalized.gif", "wb") as f:
    f.write(add_name_to_gif("EIF.gif", "نورة الفرم").read())
print("✅ GIF with correct Arabic and placement generated!")
