import io
import os
import textwrap
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def create_quote_image(message, author):
    # --- Configuration ---
    width, height = 1200, 800 
    # Chemins vers les variantes de polices
    font_bold = os.path.join("fonts", "Roboto-Bold.ttf")   # Pour la citation
    font_light = os.path.join("fonts", "Roboto-Light.ttf") # Pour l'auteur

    # 1. Fond dégradé (inchangé mais efficace)
    color_top = (255, 60, 140)    
    color_bottom = (255, 150, 120)
    base = Image.new('RGB', (width, height), color_top)
    top_layer = Image.new('RGB', (width, height), color_bottom)
    mask = Image.new('L', (width, height))
    mask_data = [int(255 * (y / height)) for y in range(height) for _ in range(width)]
    mask.putdata(mask_data)
    base.paste(top_layer, (0, 0), mask)
    
    draw = ImageDraw.Draw(base)

    # 2. Calcul dynamique avec prise en compte de l'auteur
    font_size = 110  
    max_w, max_h = width * 0.8, height * 0.7
    
    while font_size > 20:
        try:
            f_main = ImageFont.truetype(font_bold, font_size)
            # L'auteur est 40% plus petit que la citation, mais pas moins de 45px
            author_size = max(45, int(font_size * 0.5))
            f_author = ImageFont.truetype(font_light, author_size)
        except:
            f_main = f_author = ImageFont.load_default()

        # Wrap intelligent : plus la police est grosse, moins on met de mots par ligne
        chars = max(15, int(max_w / (font_size * 0.45)))
        lines = textwrap.wrap(message, width=chars)
        wrapped_q = f'“{"\n".join(lines)}”' # Utilisation de vrais guillemets typo

        # Mesures
        bq = draw.multiline_textbbox((0, 0), wrapped_q, font=f_main, align="center", spacing=12)
        wq, hq = bq[2]-bq[0], bq[3]-bq[1]
        
        txt_a = f"— {author}"
        ba = draw.textbbox((0, 0), txt_a, font=f_author)
        wa, ha = ba[2]-ba[0], ba[3]-ba[1]

        if wq <= max_w and (hq + ha + 60) <= max_h:
            break
        font_size -= 4

    # 3. Calcul de la position de départ (Centrage vertical parfait)
    spacing = 60
    total_h = hq + spacing + ha
    start_y = (height - total_h) / 2

    # 4. Ajout d'une ombre portée légère pour la lisibilité
    # On dessine le texte en noir très transparent légèrement décalé
    shadow_color = (0, 0, 0, 40)
    offset = 3
    
    # Dessin citation
    draw.multiline_text(((width-wq)/2 + offset, start_y + offset), wrapped_q, 
                        font=f_main, fill=(0,0,0,60), align="center", spacing=12)
    draw.multiline_text(((width-wq)/2, start_y), wrapped_q, 
                        font=f_main, fill="white", align="center", spacing=12)
    
    # Dessin auteur (un peu plus de transparence pour l'auteur pour le style)
    draw.text(((width-wa)/2 + offset, start_y + hq + spacing + offset), txt_a, 
              font=f_author, fill=(0,0,0,60))
    draw.text(((width-wa)/2, start_y + hq + spacing), txt_a, 
              font=f_author, fill=(255, 255, 255, 230))

    # 5. Export
    buf = io.BytesIO()
    base.save(buf, format='PNG', optimize=True)
    buf.seek(0)
    return buf