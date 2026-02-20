from PIL import Image
import io
from django.core.files.uploadedfile import InMemoryUploadedFile
import os


def compress_image(image_file, max_width=800, quality=85, format='JPEG'):
    """
    Compress an image file to reduce file size while maintaining quality.
    
    Args:
        image_file: Uploaded image file
        max_width: Maximum width for the compressed image (default: 800px)
        quality: Compression quality (1-100, default: 85)
        format: Output format (default: JPEG)
    
    Returns:
        Compressed InMemoryUploadedFile
    """
    try:
        # Open the image
        img = Image.open(image_file)
        
        # Convert RGBA to RGB for JPEG format
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        
        # Calculate new dimensions maintaining aspect ratio
        if img.width > max_width:
            ratio = max_width / img.width
            new_height = int(img.height * ratio)
            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
        
        # Save to memory buffer
        buffer = io.BytesIO()
        
        # Determine output format and extension
        if format.upper() == 'JPEG':
            output_format = 'JPEG'
            output_extension = '.jpg'
        elif format.upper() == 'PNG':
            output_format = 'PNG'
            output_extension = '.png'
        else:
            output_format = 'JPEG'
            output_extension = '.jpg'
        
        # Save with compression
        save_kwargs = {'format': output_format}
        if output_format == 'JPEG':
            save_kwargs['quality'] = quality
            save_kwargs['optimize'] = True
        
        img.save(buffer, **save_kwargs)
        buffer.seek(0)
        
        # Create new file name
        original_name = os.path.splitext(image_file.name)[0]
        new_name = f"{original_name}_compressed{output_extension}"
        
        # Create InMemoryUploadedFile
        compressed_file = InMemoryUploadedFile(
            buffer,
            None,
            new_name,
            f'image/{output_format.lower()}',
            buffer.tell(),
            None
        )
        
        return compressed_file
        
    except Exception as e:
        # If compression fails, return original file
        print(f"Image compression failed: {e}")
        return image_file


def get_image_size_reduction(original_file, compressed_file):
    """
    Calculate the size reduction percentage.
    
    Args:
        original_file: Original image file
        compressed_file: Compressed image file
    
    Returns:
        Tuple of (original_size, compressed_size, reduction_percentage)
    """
    original_size = original_file.size
    compressed_size = compressed_file.size
    
    if original_size > 0:
        reduction_percentage = ((original_size - compressed_size) / original_size) * 100
    else:
        reduction_percentage = 0
    
    return original_size, compressed_size, reduction_percentage
