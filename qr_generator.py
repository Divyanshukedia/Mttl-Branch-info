import qrcode
from PIL import Image
import os

def generate_qr_with_logo(url, logo_path, output_path="qr_with_logo.png"):
    """
    Generate a QR code for the given URL and embed a logo in the center.
    
    Args:
        url (str): The URL to encode in the QR code.
        logo_path (str): Path to the logo image file.
        output_path (str): Path to save the generated QR code image.
    """
    try:
        # Configure QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction for logo
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        # Generate QR code image
        qr_image = qr.make_image(fill_color="black", back_color="white").convert("RGBA")

        # Check if logo exists
        if os.path.exists(logo_path):
            try:
                logo = Image.open(logo_path).convert("RGBA")
            except Exception as e:
                print(f"Error opening logo: {e}. Generating QR code without logo.")
                qr_image.save(output_path)
                return

            # Resize logo to fit in the center (approx 25% of QR code size)
            qr_width, qr_height = qr_image.size
            logo_size = int(qr_width * 0.25)  # Logo is 25% of QR code width
            logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)

            # Calculate position to center the logo
            logo_position = (
                (qr_width - logo_size) // 2,
                (qr_height - logo_size) // 2
            )

            # Paste logo onto QR code
            qr_image.paste(logo, logo_position, logo)  # Use logo's alpha channel as mask
        else:
            print(f"Logo file {logo_path} not found. Generating QR code without logo.")

        # Save the final QR code
        qr_image.save(output_path)
        print(f"QR code saved as {output_path}")

    except Exception as e:
        print(f"Error generating QR code: {e}")

if __name__ == "__main__":
    # URL to encode
    url = "https://divyanshukedia.github.io/Mttl-Branch-info/dashboard.html"
    
    # Path to logo (place your logo.png in the same directory or update the path)
    logo_path = "logo.png"
    
    # Generate QR code
    generate_qr_with_logo(url, logo_path)