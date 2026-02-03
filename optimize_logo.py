from PIL import Image
import os

def optimize_image(input_path, output_path, max_width=512):
    try:
        with Image.open(input_path) as img:
            # Calculate new height to maintain aspect ratio
            width_percent = (max_width / float(img.size[0]))
            new_height = int((float(img.size[1]) * float(width_percent)))
            
            # Resize if the image is larger than max_width
            if img.size[0] > max_width:
                img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
                print(f"Resized image to {max_width}x{new_height}")
            
            # Save as WebP
            img.save(output_path, "WEBP", quality=85, optimize=True)
            
            original_size = os.path.getsize(input_path)
            new_size = os.path.getsize(output_path)
            
            print(f"Original size: {original_size / 1024 / 1024:.2f} MB")
            print(f"New size: {new_size / 1024:.2f} KB")
            print(f"Reduction: {(1 - new_size / original_size) * 100:.1f}%")
            
    except Exception as e:
        print(f"Error optimizing image: {e}")

if __name__ == "__main__":
    optimize_image("logo.png", "logo.webp")
