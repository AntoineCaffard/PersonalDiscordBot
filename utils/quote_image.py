import io
import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

def create_quote_image(message, author):

    width, height = 1200, 800 
    font_path = os.path.join("fonts", "Roboto-VariableFont_wdth,wght.ttf")

    color_top = (255, 60, 140) 
    color_bottom = (255, 150, 120)
    
    base = Image.new('RGB', (width, height), color_top)
    top_layer = Image.new('RGB', (width, height), color_bottom)
    
    mask = Image.new('L', (width, height))
    mask_data = []
    for y in range(height):
        mask_data.extend([int(255 * (y / height))] * width)
    mask.putdata(mask_data)
    
    base.paste(top_layer, (0, 0), mask)
    draw = ImageDraw.Draw(base)

    font_size = 110  
    max_text_width = width * 0.85  
    max_text_height = height * 0.6 

    full_quote = f'"{message}"'
    w_q, h_q = 0, 0

    while font_size > 20:
        try:
            font_main = ImageFont.truetype(font_path, font_size)
        except:
            font_main = ImageFont.load_default()
        chars_per_line = max(10, int(max_text_width / (font_size * 0.45)))
        lines = textwrap.wrap(message, width=chars_per_line)
        full_quote = f'"{  " ".join(lines)  }"'
        
        wrapped_text = "\n".join(lines)
        full_quote_wrapped = f'"{wrapped_text}"'
        bbox = draw.multiline_textbbox((0, 0), full_quote_wrapped, font=font_main, align="center")
        w_q, h_q = bbox[2] - bbox[0], bbox[3] - bbox[1]

        if w_q <= max_text_width and h_q <= max_text_height:
            full_quote = full_quote_wrapped
            break
        
        font_size -= 5
    try:
        font_author = ImageFont.truetype(font_path, max(60, int(font_size * 0.5)))
    except:
        font_author = ImageFont.load_default()
        
    author_text = f"- {author}"
    bbox_a = draw.textbbox((0, 0), author_text, font=font_author)
    w_a, h_a = bbox_a[2] - bbox_a[0], bbox_a[3] - bbox_a[1]
    
    spacing = 50
    total_content_height = h_q + spacing + h_a
    current_y = (height - total_content_height) / 2

    draw.multiline_text(((width - w_q) / 2, current_y), full_quote, 
                        font=font_main, fill="white", align="center", spacing=10)
    
    draw.text(((width - w_a) / 2, current_y + h_q + spacing), author_text, 
              font=font_author, fill="white")

    img_byte_arr = io.BytesIO()
    base.save(img_byte_arr, format='PNG', optimize=True)
    img_byte_arr.seek(0)
    return img_byte_arr