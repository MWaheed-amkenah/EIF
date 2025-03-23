from PIL import Image, ImageDraw, ImageFont, ImageSequence
import arabic_reshaper
from bidi.algorithm import get_display
import io

def contains_arabic(text):
    return any('\u0600' <= c <= '\u06FF' for c in text)

def reshape_arabic_text(text):
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)

def add_name_to_gif(input_gif_path, name_text, eng_font_path="29lt-bukra.ttf", ar_font_path="29lt-bukra.ttf", font_size=24):
    gif = Image.open(input_gif_path)
    frames = []
    duration = gif.info.get('duration', 100)

    font_path = ar_font_path if contains_arabic(name_text) else eng_font_path

    if contains_arabic(name_text):
        name_text = reshape_arabic_text(name_text)

    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        print("⚠️ Font not found! Using default font.")
        font = ImageFont.load_default()

    try:
        while True:
            frame = gif.copy().convert("RGBA")
            draw = ImageDraw.Draw(frame)

            width, height = frame.size
            bbox = draw.textbbox((0, 0), name_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            position_x = (width - text_width) / 2
            position_y = height - 321 - text_height / 2

            draw.text((position_x + 2, position_y + 2), name_text, font=font, fill=(0, 0, 0, 150))

            bold_offsets = [(0,0), (1,0), (0,1), (1,1)]
            for offset in bold_offsets:
                draw.text((position_x + offset[0], position_y + offset[1]), name_text, font=font, fill="black")

            frames.append(frame.convert("P"))
            gif.seek(gif.tell() + 1)
    except EOFError:
        pass

    output_bytes = io.BytesIO()
    frames[0].save(
        output_bytes,
        format='GIF',
        save_all=True,
        append_images=frames[1:],
        duration=duration,
        loop=0
    )
    output_bytes.seek(0)
    return output_bytes
