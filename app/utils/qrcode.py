
import qrcode
from io import BytesIO
import base64
from PIL import Image, ImageDraw, ImageFont

def generate_qrcode(input_str:str, str_below:str=None, as_base64:bool=False, **qrcode_params:dict):
    # Generate QR code
    qr = qrcode.QRCode(
        version=qrcode_params.get('version', 7),
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=qrcode_params.get('box_size',10),
        border=qrcode_params.get('border',4)
    )
    qr.add_data(input_str)
    qr.make(fit=True)

    img = qr.make_image(fill=qrcode_params.get('fill', 'black'), back_color=qrcode_params.get('back_color','white'))

    if str_below:
        # Convert to PIL image
        img = img.convert("RGB")

        # Create a new image with extra space for text
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default()
        text_width, text_height = draw.textsize(str_below, font)
        total_height = img.height + text_height + 10  # Add some padding

        new_img = Image.new("RGB", (img.width, total_height), "white")
        new_img.paste(img, (0, 0))
        draw = ImageDraw.Draw(new_img)
        draw.text(((img.width - text_width) / 2, img.height + 5), str_below, font=font, fill="black")
        
        img = new_img

    # Save the generated image to a BytesIO object
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    
    if as_base64:
        # Encode the image to base64
        img_io = base64.b64encode(img_io.getvalue()).decode('ascii')

    return img_io