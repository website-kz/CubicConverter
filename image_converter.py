from PIL import Image
import os

def convert_image(file_path, target_format, output_dir):
    img = Image.open(file_path).convert("RGB")
    new_filename = os.path.splitext(os.path.basename(file_path))[0] + f".{target_format}"
    output_path = os.path.join(output_dir, new_filename)
    img.save(output_path)
    return {"converted": True, "output_file": output_path}