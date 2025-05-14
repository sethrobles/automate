import os
from PIL import Image

# Folder containing your .jpg and .png files
src_folder = "images_to_convert"
# Folder to save .jpeg files
dst_folder = "convert_images"

os.makedirs(dst_folder, exist_ok=True)

for filename in os.listdir(src_folder):
    name, ext = os.path.splitext(filename)
    ext = ext.lower()
    if ext in [".jpg", ".jpeg", ".png"]:
        img_path = os.path.join(src_folder, filename)
        img = Image.open(img_path).convert("RGB")
        # Save as .jpeg
        out_path = os.path.join(dst_folder, f"{name}.jpeg")
        img.save(out_path, "JPEG", quality=95)
        print(f"Converted {filename} → {name}.jpeg")
