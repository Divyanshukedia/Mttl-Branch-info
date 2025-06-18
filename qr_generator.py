import qrcode
from PIL import Image, ImageDraw, ImageFilter
import os

def generate_branded_qr(url, logo_path, output_path="branded_qr.png"):
    try:
        # Set color theme based on your logo
        qr_color = (230, 120, 20)     # Orange shade (matches logo)
        bg_color = (200, 255, 200)    # Light green

        # Configure QR
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        # Generate QR with color
        qr_img = qr.make_image(fill_color=qr_color, back_color=bg_color).convert("RGBA")
        qr_width, qr_height = qr_img.size

        if os.path.exists(logo_path):
            logo = Image.open(logo_path).convert("RGBA")

            # Resize logo
            logo_size = int(qr_width * 0.25)
            logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)

            # Rounded white background
            bg_size = logo_size + 20
            logo_bg = Image.new("RGBA", (bg_size, bg_size), (255, 255, 255, 0))
            draw = ImageDraw.Draw(logo_bg)
            draw.rounded_rectangle((0, 0, bg_size, bg_size), radius=12, fill=(255, 255, 255, 255))

            # Drop shadow for logo background
            shadow = logo_bg.copy().filter(ImageFilter.GaussianBlur(4))
            shadow = shadow.point(lambda p: int(p * 0.4))
            shadow_pos = ((qr_width - bg_size) // 2 + 2, (qr_height - bg_size) // 2 + 2)
            qr_img.paste(shadow, shadow_pos, shadow)

            # Paste logo on top of background
            logo_bg.paste(logo, ((bg_size - logo_size) // 2, (bg_size - logo_size) // 2), logo)
            pos = ((qr_width - bg_size) // 2, (qr_height - bg_size) // 2)
            qr_img.paste(logo_bg, pos, logo_bg)

        else:
            print(f"⚠️ Logo file not found: {logo_path}. Creating QR without logo.")

        qr_img.save(output_path)
        print(f"✅ Branded QR code saved as {output_path}")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    url = "https://www.maxtranstech.com/brochure.html"
    logo_path = "6ffad9f5-e98f-46ee-bf20-c00ff645975c.png"  # Use uploaded file
    generate_branded_qr(url, logo_path)
