f----------------------rom PIL import Image
import os

def create_favicons(input_path):
    try:
        with Image.open(input_path) as img:
            # 1. Standard Favicon (32x32)
            favicon = img.resize((32, 32), Image.Resampling.LANCZOS)
            favicon.save("favicon.png", "PNG")
            print("Created favicon.png (32x32)")

            # 2. Apple Touch Icon (180x180)
            apple_icon = img.resize((180, 180), Image.Resampling.LANCZOS)
            apple_icon.save("apple-touch-icon.png", "PNG")
            print("Created apple-touch-icon.png (180x180)")

    except Exception as e:
        print(f"Error creating favicons: {e}")

if __name__ == "__main__":
    create_favicons("logo.webp")
