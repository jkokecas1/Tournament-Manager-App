from PIL import Image
import io

def resize_image(file_storage, size=(25, 25)):
    """
    Resizes an image file to the specified size.
    Args:
        file_storage: A werkzeug.datastructures.FileStorage object
        size: Tuple of (width, height)
    Returns:
        bytes: The resized image data
        str: The mimetype (e.g., 'image/png')
    """
    try:
        # file_storage.stream is a file-like object
        img = Image.open(file_storage.stream)
        
        # Resize using LANCZOS for high quality downsampling
        img = img.resize(size, Image.Resampling.LANCZOS)
        
        output = io.BytesIO()
        # Convert to RGBA to persist transparency if present (e.g. PNG)
        # If saving as JPEG, would need RGB, but PNG is safer for logos
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
            
        img.save(output, format='PNG')
        return output.getvalue(), 'image/png'
    except Exception as e:
        print(f"Error resizing image: {e}")
        # Fallback: return original content if resizing fails
        file_storage.seek(0)
        return file_storage.read(), file_storage.mimetype
